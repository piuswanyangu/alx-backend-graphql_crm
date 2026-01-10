#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Time range: last 7 days
seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

# GraphQL query
query = gql("""
query GetRecentOrders($dateFrom: DateTime!) {
  orders(orderDate_Gte: $dateFrom) {
    id
    customer {
      email
    }
    orderDate
  }
}
""")

# Transport setup
transport = RequestsHTTPTransport(
    url=GRAPHQL_URL,
    verify=False,
    retries=3,
)

client = Client(
    transport=transport,
    fetch_schema_from_transport=False,
)

# Execute query
result = client.execute(
    query,
    variable_values={"dateFrom": seven_days_ago}
)

# Log file
log_file = "/tmp/order_reminders_log.txt"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(log_file, "a") as f:
    for order in result.get("orders", []):
        order_id = order["id"]
        email = order["customer"]["email"]
        f.write(f"[{timestamp}] Order ID: {order_id}, Email: {email}\n")

print("Order reminders processed!")
