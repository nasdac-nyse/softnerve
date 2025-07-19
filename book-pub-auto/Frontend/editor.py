import streamlit as st
import requests

st.title("📚 AI-Powered Book Editor")

url = st.text_input("Enter Chapter URL")

if url and st.button("Fetch Chapter"):
    r = requests.get("http://localhost:8000/fetch/", params={"url": url})
    original = r.json().get("content", "")
    st.session_state["original"] = original

if "original" in st.session_state:
    st.subheader("Original Content")
    st.text_area("Original", value=st.session_state["original"], height=300)

    if st.button("Spin with AI"):
        r = requests.post("http://localhost:8000/spin/", json={"chapter": st.session_state["original"]})
        st.session_state["spun"] = r.json().get("spun", "")

if "spun" in st.session_state:
    st.subheader("AI-Spun Chapter")
    edited = st.text_area("Edit AI Content", value=st.session_state["spun"], height=300)

    if st.button("Save Edited Version"):
        requests.post("http://localhost:8000/save/", json={
            "chapter_id": 1,
            "content": edited,
            "author_type": "human"
        })
        st.success("Saved successfully!")
