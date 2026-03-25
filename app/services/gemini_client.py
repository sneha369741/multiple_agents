import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text
