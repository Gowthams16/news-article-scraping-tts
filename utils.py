import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
import re
from deep_translator import GoogleTranslator

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize Hugging Face models for getting summary and sentiment
summarizer = pipeline("summarization")
sentiment_analyzer = pipeline("sentiment-analysis")

def scrape_news(company_name):
    #using bing here to fetch the news articles
    url = f"https://www.bing.com/news/search?q={company_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # fetching the html content
    response = requests.get(url, headers=headers)

    #Web scraping using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initializing the articles list
    articles = []
    # Searching for the news articles using class. This will vary based on the website. Limiting to 20 articles as only few will be scrapped
    for item in soup.find_all("div", class_="news-card newsitem cardcommon", limit=20):
        try:
            title_element = item.find("a", class_="title")
            if not title_element:
                continue 
            title = title_element.text.strip() #to remove trailing and leading spaces
            link = title_element['href']
            #Fetching the single article content
            article_response = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(article_response.text, "html.parser")

            content = ""
            paragraphs = article_soup.find_all('p')
            if paragraphs:
                content = " ".join(p.text for p in paragraphs)
            else:
                div_content = article_soup.find("div", class_="article-body")
                if div_content:
                    content = div_content.text
                else:
                    article_content = article_soup.find("article")
                    if article_content:
                        content = article_content.text

            summary = summarize_content(content)
            sentiment = sentiment_analysis(title)
            topics = extract_topics(content)

            #added content here to show if summary is not available
            articles.append({
                "title": title,
                "summary": summary,
                "content": content,
                "sentiment": sentiment,
                "topics": topics
            })
            #printing the error if the article is not processed
        except Exception as e:
            print(f"Error processing article: {e}")
            continue 

    return articles

def summarize_content(text):
    if not text:
        return ""
    #using the summarizer model to summarize the content and limiting the length of the summary for 130 characters
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def sentiment_analysis(text):
    if not text:
        return "Neutral"
    result = sentiment_analyzer(text)
    return result[0]['label']

def extract_topics(text):
    if not text:
        return []
    #using stopwords to remove the common words and extracting
    stop_words = set(stopwords.words("english"))
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    return list(set(filtered_words))[:5]

# def generate_hindi_tts(news_data):
#     summary = " ".join([article['summary'] for article in news_data])
#     #using googletrans to translate the summary to hindi
#     translator = Translator()
#     hindi_summary = translator.translate(summary, src="en", dest="hi").text
#     tts = gTTS(text=hindi_summary, lang="hi")

#     tts.save("summary.mp3")
#     return "summary.mp3"


def generate_hindi_tts(news_data):
    english_summary = " ".join([article['summary'] for article in news_data])
    # Translate the English summary to Hindi
    try:
        hindi_summary = GoogleTranslator(source="en", target="hi").translate(english_summary)
    except Exception as e:
        print(f"Translation error: {e}")
        hindi_summary = "कुछ त्रुटि हुई। कृपया बाद में पुनः प्रयास करें।" 
    # Generate Hindi TTS
    tts = gTTS(text=hindi_summary, lang="hi", slow=False)  # Set lang="hi" for Hindi
    tts.save("summary.mp3")  # Save the audio file
    return "summary.mp3" 
