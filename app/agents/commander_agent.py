from app.services.gemini_client import ask_gemini
from app.agents.logs_agent import analyze_logs
from app.agents.metrics_agent import analyze_metrics

def commander_process(log):
    routing_prompt = f"""
Classify this log into:
- logs_issue
- metrics_issue

Log:
{log}

Output ONLY one word.
"""

    decision = ask_gemini(routing_prompt).lower()

    if "metrics" in decision:
        analysis = analyze_metrics(log)
        agent_used = "Metrics Agent"
    else:
        analysis = analyze_logs(log)
        agent_used = "Logs Agent"

    plan_prompt = f"""
Create a step-by-step investigation plan:
{analysis}
"""

    plan = ask_gemini(plan_prompt)

    return {
        "agent": agent_used,
        "analysis": analysis,
        "plan": plan
    }
