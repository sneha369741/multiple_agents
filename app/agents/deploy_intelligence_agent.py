from app.services.gemini_client import ask_gemini

def generate_resolution(context):
    prompt = f"""
Provide:
- Root cause
- Fix
- Prevention

{context}
"""
    return ask_gemini(prompt)
