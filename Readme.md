# News Summarization and Text-to-Speech Application

## Overview

This application extracts news articles related to a given company, performs sentiment analysis, and generates a Hindi text-to-speech summary.

## Usage

1. Enter a company name in the input box.
2. Click "Fetch News" to fetch and analyze news articles.
3. View the sentiment analysis and listen to the Hindi TTS summary.

## Video explanation on the project

Loom: https://www.loom.com/share/6a1aa989669b4d37bf795759d6765989?sid=97883eb7-1d4e-4447-a252-f160bd4f92f4

You will not hear the audio file played in the video because the mic was blocking it. Please run the code and test it once.

## Deployment

This application is deployed on Hugging Face Spaces and GitHub.

### Hugging Face Spaces

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/GowthamS/news-article-scrapping-tts)

### GitHub Repository

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/<your-username>/<your-repo-name>)

### Commands to run

After cloning the repo please run

```
cd news-article-scraping-tts
python -m venv venv

On Windows: venv\Scripts\activate
On Linux/Mac: On Windows: venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py

```
