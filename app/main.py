from app.simulator.log_simulator import stream_logs
from app.utils.parser import classify_log
from app.agents.commander_agent import commander_process
from app.agents.deploy_intelligence_agent import generate_resolution
from app.services.email_service import send_email

def run():
    for log in stream_logs("app/simulator/sample_logs.txt"):
        print(f"\nLOG: {log}")

        level = classify_log(log)

        if level in ["error", "warning"]:
            result = commander_process(log)
            resolution = generate_resolution(result)

            send_email(f"""
🚨 INCIDENT ALERT

Log: {log}

Agent Used: {result['agent']}

Analysis:
{result['analysis']}

Plan:
{result['plan']}

Resolution:
{resolution}
""")

if __name__ == "__main__":
    run()
