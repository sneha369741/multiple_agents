"""
agents.py — Multi-Agent AI System: Autonomous Incident Commander
Four agents powered by Groq (openai/gpt-oss-120b):

1. LogsAgent       — Forensic log analyzer, finds errors & correlations
2. MetricsAgent    — Telemetry analyst, spots CPU/memory/latency anomalies
3. DeployAgent     — Historian, maps errors to deployment events
4. CommanderAgent  — Orchestrator, runs the full investigation loop
"""

import re
from groq import Groq

GROQ_MODEL = "openai/gpt-oss-120b"

# ──────────────────────────────────────────────────────────────
# Shared Groq helper
# ──────────────────────────────────────────────────────────────

def _call_groq(api_key: str, prompt: str, system: str = "") -> str:
    client = Groq(api_key=api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=2048,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# ──────────────────────────────────────────────────────────────
# Agent 1 — LOGS AGENT
# ──────────────────────────────────────────────────────────────

LOGS_AGENT_SYSTEM = """
You are the Logs Agent — a forensic expert on application log analysis.
Your job:
1. Identify all ERROR and CRITICAL log entries.
2. Find error correlations and cascade patterns (e.g., DB timeout -> auth failure -> API outage).
3. For each distinct error type, propose a clear, actionable fix.
4. Summarize the incident timeline.

Format your output with clear sections:
## Critical & Error Events
## Cascade Analysis
## Recommended Fixes
## Incident Timeline
"""

def run_logs_agent(api_key: str, log_text: str) -> dict:
    prompt = f"""
Analyze the following application logs and provide a full incident forensic report.

=== LOGS ===
{log_text}
=== END LOGS ===
"""
    raw = _call_groq(api_key, prompt, LOGS_AGENT_SYSTEM)

    errors   = len(re.findall(r'\| ERROR\s+\|', log_text))
    warnings = len(re.findall(r'\| WARN\s+\|', log_text))
    critical = len(re.findall(r'\| CRITICAL\s+\|', log_text))

    return {
        "agent": "Logs Agent",
        "icon": "🔍",
        "summary": raw,
        "stats": {
            "errors": errors,
            "warnings": warnings,
            "critical": critical,
        }
    }


# ──────────────────────────────────────────────────────────────
# Agent 2 — METRICS AGENT
# ──────────────────────────────────────────────────────────────

METRICS_AGENT_SYSTEM = """
You are the Metrics Agent — a telemetry and performance analyst.
Your job:
1. Extract all performance metrics from logs (CPU %, memory %, latency, connection counts).
2. Detect anomalies: spikes, sustained high usage, memory leaks, latency outliers.
3. Correlate metrics anomalies with service errors.
4. Recommend infrastructure actions (scale-up, restart, alerting thresholds).

Format your output with:
## Extracted Metrics
## Anomalies Detected
## Metrics-to-Error Correlation
## Infrastructure Recommendations
"""

def run_metrics_agent(api_key: str, log_text: str) -> dict:
    metrics_lines = [
        line for line in log_text.splitlines()
        if any(kw in line.lower() for kw in [
            "cpu", "memory", "latency", "connection", "usage", "spike",
            "heap", "leak", "pool", "timeout", "ms", "%"
        ])
    ]
    focused_log = "\n".join(metrics_lines) if metrics_lines else log_text

    prompt = f"""
Analyze performance metrics and telemetry signals from these log entries.
Identify all anomalies and recommend infrastructure actions.

=== METRICS-RELATED LOG ENTRIES ===
{focused_log}
=== FULL LOG CONTEXT ===
{log_text}
"""
    raw = _call_groq(api_key, prompt, METRICS_AGENT_SYSTEM)

    cpu_values = re.findall(r'CPU usage at (\d+)%', log_text)
    mem_values = re.findall(r'[Mm]emory usage.*?(\d+)%', log_text)

    return {
        "agent": "Metrics Agent",
        "icon": "📊",
        "summary": raw,
        "stats": {
            "cpu_readings": [int(v) for v in cpu_values],
            "memory_readings": [int(v) for v in mem_values],
            "metrics_lines_found": len(metrics_lines),
        }
    }


# ──────────────────────────────────────────────────────────────
# Agent 3 — DEPLOY INTELLIGENCE AGENT
# ──────────────────────────────────────────────────────────────

DEPLOY_AGENT_SYSTEM = """
You are the Deploy Intelligence Agent — the historian of the system.
Your job:
1. Identify any deployment, version change, config change, or release events in the logs.
2. Map errors and incidents that occurred AFTER each deployment.
3. Assess whether the deployment likely caused or contributed to the incident.
4. Recommend rollback decision or post-deployment checklist.

Format your output with:
## Deployment Events Found
## Post-Deploy Error Mapping
## Causality Assessment
## Rollback Recommendation
"""

def run_deploy_agent(api_key: str, log_text: str) -> dict:
    prompt = f"""
Analyze the logs to identify deployment events and correlate them with subsequent errors.
Assess if a recent deployment caused the incident.

=== LOGS ===
{log_text}
"""
    raw = _call_groq(api_key, prompt, DEPLOY_AGENT_SYSTEM)

    deploy_events = re.findall(r'deploy.*?v[\d.]+', log_text, re.IGNORECASE)

    return {
        "agent": "Deploy Intelligence Agent",
        "icon": "🚀",
        "summary": raw,
        "stats": {
            "deploy_events": deploy_events,
        }
    }


# ──────────────────────────────────────────────────────────────
# Agent 4 — COMMANDER AGENT (Orchestrator)
# ──────────────────────────────────────────────────────────────

COMMANDER_AGENT_SYSTEM = """
You are the Commander Agent — the master orchestrator of incident response.
You receive reports from three specialist agents:
- Logs Agent (error forensics)
- Metrics Agent (performance telemetry)
- Deploy Intelligence Agent (deployment impact)

Your job:
1. Synthesize all three reports into a unified incident assessment.
2. Determine the Root Cause (primary culprit service/event).
3. Assign Severity Level: P1 (Critical) / P2 (High) / P3 (Medium).
4. Create a prioritized Action Plan with numbered steps.
5. Write an executive summary suitable for a CTO or on-call manager.

Format your output with:
## Root Cause Determination
## Severity: [P1/P2/P3]
## Executive Summary
## Prioritized Action Plan
## Prevention Recommendations
"""

def run_commander_agent(
    api_key: str,
    logs_report: str,
    metrics_report: str,
    deploy_report: str,
    log_text: str,
) -> dict:
    prompt = f"""
You are commanding an incident response. Below are the reports from your three specialist agents.
Synthesize them into a final incident command decision.

=== LOGS AGENT REPORT ===
{logs_report}

=== METRICS AGENT REPORT ===
{metrics_report}

=== DEPLOY INTELLIGENCE REPORT ===
{deploy_report}

=== ORIGINAL LOG SNIPPET (last 20 lines) ===
{chr(10).join(log_text.splitlines()[-20:])}
"""
    raw = _call_groq(api_key, prompt, COMMANDER_AGENT_SYSTEM)

    return {
        "agent": "Commander Agent",
        "icon": "🎖️",
        "summary": raw,
    }


# ──────────────────────────────────────────────────────────────
# Orchestration entry point
# ──────────────────────────────────────────────────────────────

def run_all_agents(api_key: str, log_text: str) -> dict:
    results = {}
    results["logs"]    = run_logs_agent(api_key, log_text)
    results["metrics"] = run_metrics_agent(api_key, log_text)
    results["deploy"]  = run_deploy_agent(api_key, log_text)
    results["commander"] = run_commander_agent(
        api_key,
        logs_report    = results["logs"]["summary"],
        metrics_report = results["metrics"]["summary"],
        deploy_report  = results["deploy"]["summary"],
        log_text       = log_text,
    )
    return results