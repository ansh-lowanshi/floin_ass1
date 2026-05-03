from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Google Search API Running"}


@app.get("/search")
def search(q: str):
    url = f"https://en.wikipedia.org/wiki/{q}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1")
    para = soup.find("p")

    return {
        "query": q,
        "title": title.text if title else "",
        "summary": para.text.strip() if para else ""
    }