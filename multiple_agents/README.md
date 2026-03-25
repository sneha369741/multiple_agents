# 🎖️ Autonomous Incident Commander
**Bayer AI Hackathon 2026 — Agentic AI Track**

A multi-agent AI system that autonomously investigates system incidents using Google Gemini.

---

## 🤖 Agent Architecture

```
Logs → [Logs Agent] ──────┐
       [Metrics Agent] ───┼──► [Commander Agent] → Final Verdict + Action Plan
       [Deploy Agent] ────┘
```

| Agent | Role | Focus |
|-------|------|-------|
| 🔍 **Logs Agent** | Forensic Expert | Error detection, cascade analysis, fix recommendations |
| 📊 **Metrics Agent** | Telemetry Analyst | CPU/memory/latency anomalies, infra recommendations |
| 🚀 **Deploy Agent** | Historian | CI/CD event mapping, rollback decisions |
| 🎖️ **Commander Agent** | Orchestrator | Root cause, severity, prioritized action plan |

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a free Gemini API key
→ https://aistudio.google.com/app/apikey (free tier available)

### 3. Run the app
```bash
streamlit run app.py
```

### 4. (Optional) Generate sample logs
```bash
python generate_logs.py
# Creates: sample_logs/app_logs.txt
```

---

## 📁 Project Structure
```
incident_commander/
├── app.py              # Streamlit UI
├── agents.py           # All 4 AI agents (Gemini-powered)
├── generate_logs.py    # Sample log generator
├── requirements.txt
├── sample_logs/
│   └── app_logs.txt    # Generated sample logs
└── README.md
```

---

## 🔁 Reasoning Loop
```
DETECT     → Parse incoming log stream
PLAN       → Launch specialist agents
INVESTIGATE → Each agent deep-scans its domain
DECIDE     → Commander synthesises findings
ACT        → Prioritized action plan generated
REPORT     → Executive summary + downloadable report
```

---

## 💡 Key Features
- **Upload any log file** (.txt / .log) or paste logs directly
- **4 AI agents** running in sequence with Gemini 1.5 Flash
- **Cascade analysis**: detects how one failure triggers another
- **Metrics extraction**: pulls CPU/memory numbers directly from logs
- **Deploy correlation**: links errors to deployment events
- **Download report** as markdown after investigation
