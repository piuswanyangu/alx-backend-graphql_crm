from datetime import datetime
import requests

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5minutes
    to confirm CRM application health
    """

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # append heartbeat log
    with open(LOG_FILE, "a") as file:
        file.write(message)

    # verify Graphql endpoint
    try:
        response = request.post(
            GRAPHQL_URL,
            json={"query": "{hello}"},
            timeout=5
        )
        response.raise_for_status()
    except Exception:
        # silent fail: heartbeat should never crash cron
        pass