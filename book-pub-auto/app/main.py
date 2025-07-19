from fastapi import FastAPI, Body
from app.fetcher import fetch_content
from app.spinner import spin_text
from app.revisions import save_revision

app = FastAPI()

@app.get("/fetch/")
def fetch(url: str):
    content = fetch_content(url)
    return {"content": content}

@app.post("/spin/")
def spin(chapter: str = Body(...)):
    spun = spin_text(chapter)
    return {"spun": spun}

@app.post("/save/")
def save(chapter_id: int, content: str, author_type: str):
    save_revision(chapter_id, content, author_type)
    return {"status": "saved"}
