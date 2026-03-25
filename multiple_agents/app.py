"""
app.py — Autonomous Incident Commander
Streamlit UI for the Multi-Agent AI System

Run: streamlit run app.py
"""

import streamlit as st
import os
import time
from agents import run_logs_agent, run_metrics_agent, run_deploy_agent, run_commander_agent

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Autonomous Incident Commander",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Rajdhani:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
}

.main { background-color: #FFFFFF; }

.stApp {
    background: linear-gradient(135deg, #FFFFFF 0%, #0d1421 50%, #FFFFFF 100%);
}

h1, h2, h3 {
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 1px;
}

.agent-card {
    background: linear-gradient(135deg, #0f1923 0%, #111d2e 100%);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #00d4ff;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}

.agent-card.commander {
    border-left-color: #ff6b35;
    background: linear-gradient(135deg, #1a0f0a 0%, #1f1208 100%);
}

.agent-card.logs { border-left-color: #ff4757; }
.agent-card.metrics { border-left-color: #2ed573; }
.agent-card.deploy { border-left-color: #ffa502; }

.stat-pill {
    display: inline-block;
    background: rgba(0,212,255,0.12);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    color: #00d4ff;
    margin-right: 6px;
    margin-bottom: 6px;
}

.stat-pill.red { background: rgba(255,71,87,0.12); border-color: rgba(255,71,87,0.3); color: #ff4757; }
.stat-pill.green { background: rgba(46,213,115,0.12); border-color: rgba(46,213,115,0.3); color: #2ed573; }
.stat-pill.orange { background: rgba(255,165,2,0.12); border-color: rgba(255,165,2,0.3); color: #ffa502; }

.status-badge {
    display: inline-block;
    padding: 4px 16px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.title-block {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem;
}

.stTextArea textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem;
    background: #0a0e17 !important;
    color: #7ecfff !important;
    border: 1px solid #1e3a5f !important;
}

div[data-testid="stExpander"] {
    border: 1px solid #1e3a5f;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎖️ Incident Commander")
    st.markdown("---")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="AIza...",
        help="Get a free key at https://console.groq.com/keys"
    )

    st.markdown("---")
    st.markdown("### 🤖 Agent Pipeline")
    st.markdown("""
    ```
    [Logs Agent]    ──┐
    [Metrics Agent] ──┼──► [Commander]
    [Deploy Agent]  ──┘
    ```
    """)

    st.markdown("---")
    st.markdown("### 📌 Agent Roles")
    roles = {
        "🔍 Logs Agent": "Forensic error analysis & cascade detection",
        "📊 Metrics Agent": "CPU/memory/latency anomaly detection",
        "🚀 Deploy Agent": "Maps errors to CI/CD events",
        "🎖️ Commander": "Orchestrates & delivers final verdict",
    }
    for name, desc in roles.items():
        st.markdown(f"**{name}**  \n_{desc}_")

    st.markdown("---")
    run_individual = st.checkbox("Run agents individually (show progress)", value=True)


# ─── Main Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
    <h1 style="font-size:2.8rem; color:#00d4ff; margin-bottom:0; font-family:Rajdhani,sans-serif; letter-spacing:3px;">
        🎖️ AUTONOMOUS INCIDENT COMMANDER
    </h1>
    <p style="color:#4a7fa5; font-size:1rem; margin-top:4px; font-family:JetBrains Mono,monospace;">
        BAYER AI HACKATHON 2026 // AGENTIC AI TRACK // MULTI-AGENT REASONING SYSTEM
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── Log Input ──────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### 📂 Log Input")
    input_method = st.radio("Source", ["Upload log file", "Paste logs", "Use sample logs"], horizontal=True)

    log_text = ""

    if input_method == "Upload log file":
        uploaded = st.file_uploader("Drop a .txt or .log file", type=["txt", "log"])
        if uploaded:
            raw_bytes = uploaded.read()
            log_text = raw_bytes.decode("utf-8", errors="replace")
            st.success(f"✅ Loaded {len(log_text.splitlines())} lines")

    elif input_method == "Paste logs":
        log_text = st.text_area("Paste your logs here", height=250, placeholder="2026-03-25 10:00:01 | ERROR | ...")

    else:  # Sample logs
        sample = """2026-03-25 10:00:01 | INFO     | auth-service         | Service started successfully
2026-03-25 10:00:05 | INFO     | db-service           | Database connection established
2026-03-25 10:00:10 | INFO     | api-gateway          | Incoming request /login
2026-03-25 10:00:12 | INFO     | auth-service         | User authentication successful
2026-03-25 10:01:02 | WARN     | db-service           | Connection pool nearing limit
2026-03-25 10:01:10 | INFO     | api-gateway          | Incoming request /getUserData
2026-03-25 10:01:15 | ERROR    | db-service           | Database connection timeout
2026-03-25 10:01:16 | ERROR    | auth-service         | Failed to fetch user data from DB
2026-03-25 10:01:18 | WARN     | api-gateway          | Response delayed (latency > 1000ms)
2026-03-25 10:02:01 | INFO     | scheduler-service    | Running background job: data-sync
2026-03-25 10:02:10 | ERROR    | scheduler-service    | Data sync failed due to network issue
2026-03-25 10:02:20 | INFO     | api-gateway          | Incoming request /checkout
2026-03-25 10:02:22 | ERROR    | payment-service      | Payment API failed: 502 Bad Gateway
2026-03-25 10:02:23 | WARN     | api-gateway          | Retrying request /checkout
2026-03-25 10:02:40 | INFO     | api-gateway          | Incoming request /checkout
2026-03-25 10:02:42 | ERROR    | payment-service      | Payment API timeout
2026-03-25 10:02:45 | ERROR    | api-gateway          | Checkout failed after retries
2026-03-25 10:03:01 | INFO     | monitoring-service   | CPU usage at 88%
2026-03-25 10:03:05 | WARN     | monitoring-service   | Memory usage high (85%)
2026-03-25 10:03:10 | ERROR    | monitoring-service   | CPU spike detected (95%)
2026-03-25 10:03:15 | ERROR    | api-gateway          | Request failed due to timeout
2026-03-25 10:03:30 | INFO     | deploy-service       | New version v2.1 deployed
2026-03-25 10:03:40 | ERROR    | auth-service         | Increased login failures detected
2026-03-25 10:04:00 | ERROR    | db-service           | Too many connections
2026-03-25 10:04:05 | ERROR    | auth-service         | Authentication service degraded
2026-03-25 10:04:20 | INFO     | monitoring-service   | CPU usage at 97%
2026-03-25 10:04:25 | ERROR    | monitoring-service   | Memory leak suspected
2026-03-25 10:04:40 | CRITICAL | api-gateway          | Service unavailable (503)
2026-03-25 10:04:45 | CRITICAL | system               | Major outage detected"""
        log_text = sample
        st.text_area("Sample logs (editable)", value=sample, height=250)

with col_right:
    st.markdown("### 🧭 Reasoning Loop")
    st.markdown("""
    <div style="background:#0f1923; border:1px solid #1e3a5f; border-radius:8px; padding:1rem; font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:#7ecfff;">
    <span style="color:#ff4757">DETECT</span> → Parse incoming log stream<br>
    <span style="color:#ffa502">PLAN</span>&nbsp;&nbsp;&nbsp;→ Launch specialist agents in parallel<br>
    <span style="color:#00d4ff">INVESTIGATE</span> → Each agent deep-scans its domain<br>
    <span style="color:#2ed573">DECIDE</span> → Commander synthesizes findings<br>
    <span style="color:#ff6b35">ACT</span>&nbsp;&nbsp;&nbsp;&nbsp;→ Prioritized action plan generated<br>
    <span style="color:#a29bfe">REPORT</span> → Executive summary delivered<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("&nbsp;")

    if log_text:
        import re
        total = len(log_text.splitlines())
        errors = len(re.findall(r'\| ERROR\s+\|', log_text))
        warns  = len(re.findall(r'\| WARN\s+\|', log_text))
        crits  = len(re.findall(r'\| CRITICAL\s+\|', log_text))
        st.markdown(f"""
        <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:8px;">
            <span class="stat-pill">{total} lines</span>
            <span class="stat-pill red">{errors} errors</span>
            <span class="stat-pill orange">{warns} warnings</span>
            <span class="stat-pill red">{crits} critical</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─── Run Button ─────────────────────────────────────────────────────────────────
col_btn, col_info = st.columns([1, 3])
with col_btn:
    run_clicked = st.button("🚀 Launch Investigation", use_container_width=True, type="primary")
with col_info:
    if not api_key:
        st.warning("⚠️ Enter your Groq API key in the sidebar to run agents.")
    elif not log_text.strip():
        st.warning("⚠️ Provide log data above to begin.")
    else:
        st.info("✅ Ready — click Launch Investigation to start all 4 agents.")

# ─── Agent Execution ─────────────────────────────────────────────────────────────
if run_clicked:
    if not api_key:
        st.error("❌ No API key provided. Add your Groq API key in the sidebar.")
        st.stop()
    if not log_text.strip():
        st.error("❌ No log data provided.")
        st.stop()

    st.markdown("## 🔄 Agent Investigation in Progress")
    results = {}

    # ── Agent 1: Logs ─────────────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="agent-card logs">', unsafe_allow_html=True)
        st.markdown("#### 🔍 Logs Agent — Forensic Error Analysis")
        with st.spinner("Deep-scanning logs for error patterns and cascades..."):
            try:
                t0 = time.time()
                results["logs"] = run_logs_agent(api_key, log_text)
                elapsed = time.time() - t0
                st.success(f"✅ Logs Agent completed in {elapsed:.1f}s")

                stats = results["logs"]["stats"]
                st.markdown(f"""
                <span class="stat-pill red">{stats['errors']} errors</span>
                <span class="stat-pill orange">{stats['warnings']} warnings</span>
                <span class="stat-pill red">{stats['critical']} critical</span>
                """, unsafe_allow_html=True)

                with st.expander("📄 Logs Agent Report", expanded=True):
                    st.markdown(results["logs"]["summary"])
            except Exception as e:
                st.error(f"Logs Agent error: {e}")
                results["logs"] = {"summary": f"Agent failed: {e}", "stats": {}}
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("&nbsp;")

    # ── Agent 2: Metrics ──────────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="agent-card metrics">', unsafe_allow_html=True)
        st.markdown("#### 📊 Metrics Agent — Telemetry & Anomaly Detection")
        with st.spinner("Analysing CPU, memory, latency signals..."):
            try:
                t0 = time.time()
                results["metrics"] = run_metrics_agent(api_key, log_text)
                elapsed = time.time() - t0
                st.success(f"✅ Metrics Agent completed in {elapsed:.1f}s")

                stats = results["metrics"]["stats"]
                cpu_str  = ", ".join(f"{v}%" for v in stats.get("cpu_readings", []))
                mem_str  = ", ".join(f"{v}%" for v in stats.get("memory_readings", []))
                if cpu_str:
                    st.markdown(f'<span class="stat-pill">CPU: {cpu_str}</span>', unsafe_allow_html=True)
                if mem_str:
                    st.markdown(f'<span class="stat-pill orange">Mem: {mem_str}</span>', unsafe_allow_html=True)

                with st.expander("📄 Metrics Agent Report", expanded=True):
                    st.markdown(results["metrics"]["summary"])
            except Exception as e:
                st.error(f"Metrics Agent error: {e}")
                results["metrics"] = {"summary": f"Agent failed: {e}", "stats": {}}
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("&nbsp;")

    # ── Agent 3: Deploy ───────────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="agent-card deploy">', unsafe_allow_html=True)
        st.markdown("#### 🚀 Deploy Intelligence Agent — CI/CD Impact Analysis")
        with st.spinner("Mapping deployment events to error timelines..."):
            try:
                t0 = time.time()
                results["deploy"] = run_deploy_agent(api_key, log_text)
                elapsed = time.time() - t0
                st.success(f"✅ Deploy Agent completed in {elapsed:.1f}s")

                events = results["deploy"]["stats"].get("deploy_events", [])
                if events:
                    st.markdown(f'<span class="stat-pill orange">{len(events)} deploy event(s) found</span>', unsafe_allow_html=True)

                with st.expander("📄 Deploy Intelligence Report", expanded=True):
                    st.markdown(results["deploy"]["summary"])
            except Exception as e:
                st.error(f"Deploy Agent error: {e}")
                results["deploy"] = {"summary": f"Agent failed: {e}", "stats": {}}
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Agent 4: Commander ────────────────────────────────────────────────────
    st.markdown("## 🎖️ Commander Agent — Final Verdict")
    with st.container():
        st.markdown('<div class="agent-card commander">', unsafe_allow_html=True)
        with st.spinner("Commander synthesising all agent reports into final incident decision..."):
            try:
                t0 = time.time()
                results["commander"] = run_commander_agent(
                    api_key,
                    logs_report    = results["logs"]["summary"],
                    metrics_report = results["metrics"]["summary"],
                    deploy_report  = results["deploy"]["summary"],
                    log_text       = log_text,
                )
                elapsed = time.time() - t0
                st.success(f"✅ Commander Agent completed in {elapsed:.1f}s")
                st.markdown(results["commander"]["summary"])
            except Exception as e:
                st.error(f"Commander Agent error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Export ────────────────────────────────────────────────────────────────
    st.markdown("### 💾 Export Report")
    full_report = f"""# AUTONOMOUS INCIDENT COMMANDER — REPORT
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}

## 🔍 LOGS AGENT REPORT
{results['logs']['summary']}

{'='*60}

## 📊 METRICS AGENT REPORT
{results['metrics']['summary']}

{'='*60}

## 🚀 DEPLOY INTELLIGENCE REPORT
{results['deploy']['summary']}

{'='*60}

## 🎖️ COMMANDER — FINAL VERDICT
{results['commander']['summary']}
"""
    st.download_button(
        "⬇️ Download Full Report (.md)",
        data=full_report,
        file_name=f"incident_report_{time.strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown",
    )

# ─── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#2a4a6e; font-size:0.75rem; font-family:JetBrains Mono,monospace;'>"
    "BAYER AI HACKATHON 2026 // AGENTIC AI TRACK // AUTONOMOUS INCIDENT COMMANDER</p>",
    unsafe_allow_html=True
)
