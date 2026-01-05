import pytest
from graphene.test import Client
from django.contrib.auth.models import User

from alx_backend_graphql.schema import schema # type: ignore
from crm.models import Customer, Product, Order

# test create customer mutation
@pytest.mark.django_db
def test_create_customer():
    client = Client(schema)

    mutation = """
    mutation {
      createCustomer(input: {
        name: "Alice",
        email: "alice@test.com",
        phone: "+1234567890"
      }) {
        customer {
          id
          name
          email
        }
        message
      }
    }
    """

    response = client.execute(mutation)

    assert response["data"]["createCustomer"]["customer"]["email"] == "alice@test.com"
    assert Customer.objects.count() == 1
