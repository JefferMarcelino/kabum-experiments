import json

with open("entity_rank.json", 'r', encoding='utf-8') as file:
  data = json.load(file)

for post in data[:10]:
  print(f"{post['position']}. {post['entity']} - {post['mentions']} menções")