import requests
from bs4 import BeautifulSoup

def fetch_content(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.select_one("div.chapter-content")  # Update selector as needed
    return content.get_text(strip=True) if content else "No content found."
