import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Load and chunk the data
def load_text_chunks(file_path, chunk_size=500, overlap=100):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks

chunks = load_text_chunks("data/rita_notes.txt")

# 2. Merge top relevant chunks into context (basic simulated retrieval)
context = "\n\n".join(chunks)

# 3. Gemini-based chatbot loop
model = genai.GenerativeModel("models/gemini-2.0-flash")

print("🧠 Dementia RAG Chat (Gemini)\nType 'exit' to quit.")

while True:
    query = input("\nAsk about patient care: ")
    if query.lower() in ['exit', 'quit']:
        break

    prompt = f"""
You are a dementia caregiver assistant. Use the context provided below to answer the question.

CONTEXT:
{context}

QUESTION:
{query}

Answer based **only** on the context. If unsure, say "I don't know based on the data."
"""

    response = model.generate_content(prompt)
    print(f"\n🤖 {response.text.strip()}")
