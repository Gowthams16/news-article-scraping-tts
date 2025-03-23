import streamlit as st
import requests
from utils import scrape_news, summarize_content, sentiment_analysis, generate_hindi_tts
from api import get_news

# To create title of the app
st.title("News Summarization and Sentiment Analysis")

# To create input text field
company_name = st.text_input("Enter Company Name", "Tesla")

# To create a button and also add a loading spinner
if st.button("Fetch News"):
    with st.spinner("Fetching news articles..."):
        news_data = get_news(company_name) #fetching the news
        
        if not news_data:
            st.error("No news articles found. Please try another company.")
        else:
            st.success(f"Fetched {len(news_data)} articles for {company_name}.")

            #Writing the data in the Streamlit app

            st.subheader("News Articles and Sentiment Analysis")
            for idx, article in enumerate(news_data):
                st.write(f"**Article {idx + 1}**")
                st.write(f"**Title:** {article['title']}")
                st.write(f"**Content:** {article['content']}")
                st.write(f"**Summary:** {article['summary']}")
                st.write(f"**Sentiment:** {article['sentiment']}")
                st.write(f"**Topics:** {', '.join(article['topics'])}")
                st.write("---")

            #Sentiment Analysis

            st.subheader("Sentiment Analysis")
            sentiment_distribution = {
                "Positive": sum(1 for article in news_data if article['sentiment'].lower() == "positive"),
                "Negative": sum(1 for article in news_data if article['sentiment'].lower() == "negative"),
                "Neutral": sum(1 for article in news_data if article['sentiment'].lower() == "neutral")
            }
            st.write(f"**Sentiment Distribution:** {sentiment_distribution}")

            #Text to speech in hindi

            st.subheader("Hindi Text-to-Speech Summary")
            tts_file = generate_hindi_tts(news_data)
            st.audio(tts_file, format="audio/mp3")