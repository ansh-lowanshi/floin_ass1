from fastapi import FastAPI
from playwright.sync_api import sync_playwright

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Google Search API Running"}

@app.get("/search")
def search(q: str):
    summary = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = browser.new_page()

        page.goto("https://www.wikipedia.org/")
        page.fill('input[name="search"]', q)
        page.keyboard.press("Enter")

        page.wait_for_timeout(3000)

        title_el = page.query_selector("h1")

        paragraphs = page.query_selector_all(
            "#mw-content-text p"
        )

        for para in paragraphs:
            text = para.inner_text().strip()

            if len(text) > 50:
                summary = text
                break

        result = {
            "query": q,
            "title": title_el.inner_text().strip() if title_el else "",
            "summary": summary
        }

        browser.close()

    return result