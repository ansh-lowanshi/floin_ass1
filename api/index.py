from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Google Search API Running"}


@app.get("/search")
def search(q: str):
    search_url = f"https://en.wikipedia.org/w/index.php?search={quote(q)}"

    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1")
    paragraphs = soup.find_all("p")

    summary = ""

    for p in paragraphs:
        text = p.get_text().strip()
        if len(text) > 60:
            summary = text
            break

    return {
        "query": q,
        "title": title.get_text().strip() if title else "",
        "summary": summary
    }