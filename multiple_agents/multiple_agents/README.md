
#  Autonomous Incident Commander

our AI system detects,investigates and resolves system failures using logs & metrics.



##  What it does

* Reads logs and metrics
* Detects system issues
* Finds root cause
* Suggests solution

---

##  Tech Stack

* Python
* LLM (OpenRouter / Mistral)
* FastAPI
* Docker

---

## examples Files

```
main.py        # API
app.py         # Logic
logs.txt       # Sample logs
metrics.json   # Sample metrics
Dockerfile
```

---


##  Run with Docker

```bash
docker build -t incident-ai .
docker run -p 8000:8000 incident-ai
```

---

##  Example

Logs:

```
ERROR: DB connection timeout
```

Metrics:

```
Latency: 2000ms
```

Output:

```
Issue: DB failure
Root Cause: Connection timeout
Fix: Check DB or rollback deployment
```

