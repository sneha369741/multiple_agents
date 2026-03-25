from app.services.gemini_client import ask_gemini

def analyze_metrics(log):
    prompt = f"Analyze metrics issue (memory, latency): {log}"
    return ask_gemini(prompt)
