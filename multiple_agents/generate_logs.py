"""
Log Generator — produces realistic application logs for demo/testing.
Run: python generate_logs.py
Generates: sample_logs/app_logs.txt
"""

import random
import datetime
import os

SERVICES = ["auth-service", "db-service", "api-gateway", "payment-service",
            "scheduler-service", "monitoring-service", "deploy-service", "cache-service"]

LOG_LEVELS = ["INFO", "WARN", "ERROR", "CRITICAL"]

# Weighted so INFO is most common, CRITICAL is rare
LEVEL_WEIGHTS = [60, 20, 15, 5]

SCENARIOS = [
    # (level, service, message)
    ("INFO",     "auth-service",       "Service started successfully"),
    ("INFO",     "db-service",         "Database connection established"),
    ("INFO",     "api-gateway",        "Incoming request /login"),
    ("INFO",     "api-gateway",        "Incoming request /getUserData"),
    ("INFO",     "api-gateway",        "Incoming request /checkout"),
    ("INFO",     "scheduler-service",  "Running background job: data-sync"),
    ("INFO",     "deploy-service",     "New version v2.1 deployed"),
    ("INFO",     "monitoring-service", "CPU usage at 45%"),
    ("INFO",     "cache-service",      "Cache hit ratio: 92%"),
    ("INFO",     "auth-service",       "User authentication successful"),
    ("INFO",     "db-service",         "Query executed in 12ms"),
    ("WARN",     "db-service",         "Connection pool nearing limit (80%)"),
    ("WARN",     "api-gateway",        "Response delayed (latency > 1000ms)"),
    ("WARN",     "monitoring-service", "Memory usage high (85%)"),
    ("WARN",     "cache-service",      "Cache eviction rate increasing"),
    ("WARN",     "auth-service",       "Multiple failed login attempts from IP 192.168.1.x"),
    ("ERROR",    "db-service",         "Database connection timeout"),
    ("ERROR",    "auth-service",       "Failed to fetch user data from DB"),
    ("ERROR",    "scheduler-service",  "Data sync failed due to network issue"),
    ("ERROR",    "payment-service",    "Payment API failed: 502 Bad Gateway"),
    ("ERROR",    "payment-service",    "Payment API timeout after 30s"),
    ("ERROR",    "api-gateway",        "Checkout failed after retries"),
    ("ERROR",    "monitoring-service", "CPU spike detected (95%)"),
    ("ERROR",    "auth-service",       "Increased login failures detected"),
    ("ERROR",    "db-service",         "Too many connections (limit: 100)"),
    ("ERROR",    "auth-service",       "Authentication service degraded"),
    ("ERROR",    "monitoring-service", "Memory leak suspected in heap"),
    ("CRITICAL", "api-gateway",        "Service unavailable (503)"),
    ("CRITICAL", "system",             "Major outage detected"),
    ("CRITICAL", "db-service",         "Primary DB unreachable — failover triggered"),
    ("CRITICAL", "payment-service",    "All payment gateways offline"),
]


def generate_logs(num_lines: int = 60, output_path: str = "sample_logs/app_logs.txt"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    start_time = datetime.datetime(2026, 3, 25, 10, 0, 0)
    lines = []

    for i in range(num_lines):
        start_time += datetime.timedelta(seconds=random.randint(1, 15))
        ts = start_time.strftime("%Y-%m-%d %H:%M:%S")

        # Pick a scenario or generate a random one
        if random.random() < 0.75:
            level, service, message = random.choice(SCENARIOS)
        else:
            level = random.choices(LOG_LEVELS, weights=LEVEL_WEIGHTS)[0]
            service = random.choice(SERVICES)
            message = f"Generic event [{random.randint(1000, 9999)}]"

        padding = " " * max(0, 10 - len(level))
        lines.append(f"{ts} | {level}{padding}| {service:<20} | {message}")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"✅ Generated {num_lines} log lines → {output_path}")
    return output_path


if __name__ == "__main__":
    generate_logs(num_lines=80)
