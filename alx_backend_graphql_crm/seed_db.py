from crm.models import Customer, Product

Customer.objects.create(
    name="Seed User",
    email="seed@example.com",
    phone="+254792342944"
)

Product.objects.create(
    name="Phone",
    price=500,
    stock=5
)