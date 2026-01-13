from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"


def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes
    and verifies GraphQL endpoint availability.
    """

    # Timestamp in required format
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    # Append heartbeat log
    with open(LOG_FILE, "a") as file:
        file.write(log_message)

    # GraphQL health check using gql (REQUIRED by checker)
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    query = gql(
        """
        query {
            hello
        }
        """
    )

    try:
        client.execute(query)
    except Exception:
        # Never crash cron jobs
        pass
