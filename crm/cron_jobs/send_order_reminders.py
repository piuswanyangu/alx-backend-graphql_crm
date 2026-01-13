#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Log file path
LOG_FILE = "/tmp/order_reminders_log.txt"


def main():
    # 1. Calculate date range (last 7 days)
    today = datetime.utcnow()
    last_week = today - timedelta(days=7)

    # Convert to ISO format (GraphQL-friendly)
    last_week_iso = last_week.isoformat()

    # 2. Setup GraphQL transport
    transport = RequestsHTTPTransport(
        url=GRAPHQL_URL,
        verify=True,
        retries=3,
    )

    # 3. Create GraphQL client
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # 4. GraphQL query
    query = gql(
        """
        query GetRecentOrders($orderDate: DateTime!) {
            orders(orderDate_Gte: $orderDate) {
                id
                customer {
                    email
                }
            }
        }
        """
    )

    # 5. Execute query
    result = client.execute(
        query,
        variable_values={"orderDate": last_week_iso}
    )

    # 6. Write results to log file
    with open(LOG_FILE, "a") as log_file:
        for order in result.get("orders", []):
            log_entry = (
                f"{datetime.utcnow().isoformat()} | "
                f"Order ID: {order['id']} | "
                f"Customer Email: {order['customer']['email']}\n"
            )
            log_file.write(log_entry)

    # 7. Console output
    print("Order reminders processed!")


if __name__ == "__main__":
    main()
