import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Default context from fallback file
def load_context(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# App UI
st.set_page_config(page_title="Dementia Care Chat", page_icon="🧠")
st.title("🧠 Dementia Care Assistant (RAG + Gemini)")
st.markdown("Ask questions about patient behavior, routines, and care tips based on your uploaded notes.")

# Upload section
uploaded_file = st.file_uploader("📂 Upload Patient Notes (.txt)", type="txt")

if uploaded_file:
    context = uploaded_file.read().decode("utf-8")
else:
    st.info("No file uploaded. Using default patient file.")
    context = load_context("data/rita_notes.txt")

# Input box
user_input = st.text_input("💬 Ask a question about patient care:")

# Gemini RAG Answer
if user_input:
    with st.spinner("Thinking..."):
        prompt = f"""
You are a dementia caregiver assistant. Use the context provided below to answer the question.

CONTEXT:
{context}

QUESTION:
{user_input}

Answer based mainly on the context. If unsure, be gentle and say so.do not use long words which can overwhelm, say clear , to the point yet gentlr answers
"""
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content([prompt])
        st.success("🤖 " + response.text.strip())
