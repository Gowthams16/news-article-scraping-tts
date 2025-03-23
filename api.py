from fastapi import FastAPI
from utils import scrape_news

app = FastAPI()

#using post here to get the company name and to process the request
@app.post("/get_news")
def get_news(request):
    news_data = scrape_news(request)
    return news_data