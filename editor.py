import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from ebooklib import epub
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

st.set_page_config(page_title="AI Book Chapter Editor", layout="wide")
st.title("📘 AI-Powered Book Chapter Editor ")

# Step 1: Fetch chapter content from URL
st.header("Step 1: Fetch Chapter from URL")
url = st.text_input("Enter the chapter URL")

def fetch_chapter(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50)
        return text if text else "[No usable paragraph content found]"
    except Exception as e:
        return f"[Error fetching content: {str(e)}]"

if st.button("Fetch Chapter"):
    st.session_state["original"] = fetch_chapter(url)

# Step 2: Show original and generate AI version
if "original" in st.session_state:
    st.header("Step 2: Spin Chapter with Gemini")
    st.subheader("Original Chapter")
    st.text_area("Original Content", value=st.session_state["original"], height=300)

    if st.button("Spin with AI"):
        prompt = f"Rewrite this chapter in a more creative tone:\n\n{st.session_state['original']}"
        try:
            response = model.generate_content(prompt)
            spun_text = response.text.strip()
            st.session_state["spun"] = spun_text
        except Exception as e:
            st.error(f"Gemini API Error: {str(e)}")

# Step 3: Human edits and export
if "spun" in st.session_state:
    st.header("Step 3: Edit and Save")
    edited = st.text_area("Edit AI-Rewritten Chapter", value=st.session_state["spun"], height=300)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save as TXT"):
            with open("chapter_edited.txt", "w", encoding="utf-8") as f:
                f.write(edited)
            st.success("Saved as chapter_edited.txt")

    with col2:
        if st.button("📘 Export as EPUB"):
            book = epub.EpubBook()
            book.set_identifier("id123456")
            book.set_title("My AI-Spun Chapter")
            book.set_language("en")

            c1 = epub.EpubHtml(title='Chapter 1', file_name='chap_1.xhtml', lang='en')
            c1.content = f"<h1>Chapter 1</h1><p>{edited}</p>"
            book.add_item(c1)
            book.spine = ['nav', c1]
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())

            epub.write_epub("my_chapter.epub", book)
            st.success("Exported as my_chapter.epub")
