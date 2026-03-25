from app.services.gemini_client import ask_gemini

def analyze_logs(log):
    prompt = f"Analyze this log and find root cause: {log}"
    return ask_gemini(prompt)
