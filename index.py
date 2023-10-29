import requests
import json
from collections import defaultdict
import spacy
import os
import nltk
import concurrent.futures
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.util import ngrams


BASE_URL = "http://localhost:3000"
MAX_CONCURRENT_REQUESTS = 8

def fetch_post_data(id):
  print("Now fetching", id)

  try:
    response = requests.get(f"{BASE_URL}/post/{id}")
    data = response.json()
    postData = data.get('post', {})
    content = " ".join(postData.get('content', []))
    return {'id': id, **postData, 'content': content}
  except Exception as error:
    print("Error:", error)
    return None

def fetch_all_posts():
  try:
    response = requests.get(f"{BASE_URL}/all")
    data = response.json()
    allPosts = data.get('result', {}).get('posts', [])

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
      responses = list(executor.map(fetch_post_data, [post['id'] for post in allPosts if 'id' in post]))

    responses = [response for response in responses if response is not None and "title" in response]

    with open("kabumPostsData.json", 'w', encoding='utf-8') as file:
      json.dump(responses, file, indent=2, ensure_ascii=False)

    print("Data saved to kabumPostsData.json")
  except Exception as error:
    print("Error:", error)

def generate_mentions_rank_json(posts, output_file):
  print("Generating the rank")

  nlp = spacy.load("pt_core_news_lg")
  entity_count = defaultdict(int)

  for post in posts:
    combined_text = post['title'] + " " + post['content']

    doc = nlp(combined_text)
    for ent in doc.ents:
      entity_count[ent.text] += 1

  ranked_entities = sorted(entity_count.items(), key=lambda x: x[1], reverse=True)

  rank_data = []

  for i, (entity, count) in enumerate(ranked_entities, 1):
    entity_info = {
      "position": i,
      "entity": entity,
      "mentions": count
    }
    rank_data.append(entity_info)

  with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(rank_data, file, ensure_ascii=False, indent=2)

  print(f"Rank data saved to {output_file}")

def extract_most_used_words_and_phrases(posts, output_file):
  print("Extracting most used words and phrases")
  
  all_text = " ".join([f"{post['title']} {post['content']}" for post in posts])

  words = nltk.word_tokenize(all_text)
  filtered_words = [word for word in words if word.lower() not in stopwords.words('portuguese')]

  word_freq = Counter(filtered_words)

  phrases = list(ngrams(filtered_words, 2)) + list(ngrams(filtered_words, 3))
  phrase_freq = Counter(phrases)

  combined_freq = {str(key): value for key, value in dict(word_freq).items()}
  combined_freq.update({str(key): value for key, value in dict(phrase_freq).items()})

  sorted_combined_freq = dict(sorted(combined_freq.items(), key=lambda item: item[1], reverse=True))

  with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(sorted_combined_freq, file, ensure_ascii=False, indent=2)

  print(f"Most used words and phrases saved to {output_file}")


def main():
  if not os.path.exists("kabumPostsData.json"):
    fetch_all_posts()

  with open("kabumPostsData.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

  posts = data
  generate_mentions_rank_json(posts, "entity_rank.json")
  extract_most_used_words_and_phrases(posts, "most_used_words_and_phrases.json")

if __name__ == '__main__':
  main()
