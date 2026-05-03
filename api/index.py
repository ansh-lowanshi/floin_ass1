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
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(q)}"

    response = requests.get(url)

    if response.status_code != 200:
        return {
            "query": q,
            "title": "",
            "summary": "No result found"
        }

    data = response.json()

    return {
        "query": q,
        "title": data.get("title", ""),
        "summary": data.get("extract", "")
    }