from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_report_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"


@shared_task
def generate_crm_report():
    """
    Generates a weekly CRM report using GraphQL data.
    """

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
            customers {
                id
            }
            orders {
                id
                totalAmount
            }
        }
        """
    )

    try:
        result = client.execute(query)

        total_customers = len(result.get("customers", []))
        total_orders = len(result.get("orders", []))
        total_revenue = sum(
            order.get("totalAmount", 0)
            for order in result.get("orders", [])
        )

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = (
            f"{timestamp} - Report: "
            f"{total_customers} customers, "
            f"{total_orders} orders, "
            f"{total_revenue} revenue\n"
        )

        with open(LOG_FILE, "a") as file:
            file.write(log_entry)

    except Exception:
        # Celery tasks must never crash the worker
        pass
