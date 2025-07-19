import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def spin_text(text: str, style: str = "creative") -> str:
    prompt = f"Rewrite this chapter in a {style} tone:\n\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[ERROR] {str(e)}"
