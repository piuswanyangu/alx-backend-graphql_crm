from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/low_stock_updates_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"


def update_low_stock():
    """
    Runs every 12 hours to restock low inventory products
    using a GraphQL mutation.
    """

    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False
    )

    mutation = gql(
        """
        mutation {
            updateLowStockProducts {
                success
                products {
                    name
                    stock
                }
            }
        }
        """
    )

    try:
        result = client.execute(mutation)
        products = result["updateLowStockProducts"]["products"]

        with open(LOG_FILE, "a") as file:
            for product in products:
                log_line = (
                    f"{timestamp} | "
                    f"{product['name']} restocked to {product['stock']}\n"
                )
                file.write(log_line)

    except Exception:
        # Cron jobs must never crash
        pass
