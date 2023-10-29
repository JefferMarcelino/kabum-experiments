import os
import json
from gtts import gTTS
import concurrent.futures


PODCAST_FOLDER = "podcast"
MAX_WORKERS = 4

def generate_audio_for_post(post):
  post_id = post["id"]

  print(f"Generating audio for ID {post_id}")

  folder_path = f"{PODCAST_FOLDER}/{post_id}"
  os.makedirs(folder_path, exist_ok=True)

  title = post["title"]
  created_at = post["createAt"]
  published_on_message = f"Esta notícia foi publicada em {created_at}"
  content = post["content"]
  property_message = "Esta notícia é propriedade de Kabum"

  try:
    final_audio = gTTS(f"{title}\n\n{published_on_message}\n{content}\n\n{property_message}", lang="pt-br", tld="com.br")
    audio_path = os.path.join(folder_path, "original.mp3")
    final_audio.save(audio_path)
  except Exception as error:
    print(f"Error: {error}")

  text_path = os.path.join(folder_path, "transcription.txt")

  with open(text_path, "w", encoding="utf-8") as text_file:
    text_file.write(f"{title}\n")
    text_file.write(f"{created_at}\n\n")
    text_file.write(content)

def apply_ffmpeg_command(audio_path):
  temp_wav_path = audio_path.replace(".mp3", "_temp.wav")
  modified_audio_path = audio_path.replace("original.mp3", "modified.mp3")
  os.system(f"ffmpeg -i {audio_path} -filter_complex \"asetrate=32100*1.05\" -vn -ac 2 -c:a pcm_s16le {temp_wav_path}")
  os.rename(temp_wav_path, modified_audio_path)  # Rename the temp WAV file to "modified.mp3"

def collect_original_mp3_files():
  original_mp3_files = []

  for root, dirs, files in os.walk(PODCAST_FOLDER):
    for file in files:
      if file == "original.mp3":
        original_mp3_files.append(os.path.join(root, file))

  return original_mp3_files


if __name__ == "__main__":
  with open("kabumPostsData.json", "r", encoding="utf-8") as file:
    data = json.load(file)

  # I can generate 100 audios per hour
  with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(generate_audio_for_post, data)

  original_mp3_files = collect_original_mp3_files()
  with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(apply_ffmpeg_command, original_mp3_files)
