# Kabum Experiments

This repository contains code and data related to various experiments with [Kabum Digital](https://kabum.digital/) data, including the generation of JSON files and a podcast. Data is retrieved using the [unofficial-kabum-digital-api](https://github.com/JefferMarcelino/unofficial-kabum-digital-api), which must be running on your local machine.

## Files

- `entity_rank.json`: JSON file related to entity ranking.
- `kabumPostsData.json`: The main dataset used in these experiments, retrieved using the unofficial Kabum Digital API.
- `podcast/`: Contains audio files generated using the "tts.py" script.
- `tts.py`: Python script for text-to-speech (TTS) functionality, used to generate audio for the podcast.
- `index.py`: Generate all the JSON files.
- `most_used_words_and_phrases.json`: JSON file with data about the most used words and phrases.
- `requirements.txt`: Lists the required dependencies for the project.
- `view_rank.py`: Python script for viewing ranking information.

## Usage

To get started with this project, you need to have the [unofficial-kabum-digital-api](https://github.com/JefferMarcelino/unofficial-kabum-digital-api) running on your local machine. Make sure you have the necessary dependencies installed as specified in the `requirements.txt` file.

### Virtual Environment

In order to not mess with our normal environment, it's a practice to create a virtual environment which is isolated from others python libs.

1. Install virtualenv
```shell
pip install virtualenv
```
2. usage:
```shell
python<version> -m venv <virtualenv-environment-name>
```
Example:
```shell
python3 -m venv kabum-experiments-env
```
3. Activate the venv:
```shell
source <virtualenv-environment-name>/bin/activate
```
4. Deactivate the venv:
```shell
deactivate
```

### Install dependencies
```shell
pip install -r requirements.txt
```

### Key Usage Instructions
Here are some key usage instructions:

1. Use `index.py` to generate all the necessary data (JSON files).
2. Explore the data and insights in the `kabumPostsData.json` file, which is retrieved using the unofficial Kabum Digital API.
3. The "podcast" folder contains audio files generated from the text data using the `tts.py` script.
4. If you need to interact with Kabum's digital API, refer to [unofficial-kabum-digital-api](https://github.com/JefferMarcelino/unofficial-kabum-digital-api) for more details.
