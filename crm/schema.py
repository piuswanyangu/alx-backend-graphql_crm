import re
import graphene 
from graphene_django import DjangoObjectType
from django.db  import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal

from .models import Customer, Product, Order

# -------------------------------

# GRAPHQL Types

# ------------------------------

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer 
        fields = " __all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

# -----------------------------------------

# Validators

# --------------------------------------------

PHONE_REGEX  = re.compile(r"^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$")

def validate_phone(phone):
    if phone and not PHONE_REGEX.match(phone):
        raise ValidationError("Invalid Phone format")
    

    # -----------------------------------

    # MUTATION

    # --------------------------------------
class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    def mutate(self,info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")
            
        validate_phone(phone)

        customer = Customer.objects.create(
            name=name,
            email=email,
            phone=phone
            )

        return CreateCustomer(
                customer=customer,
                message="Customer created successfully"
            )
        

class BulkCustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    class Arguments:
        input = graphene.List(BulkCustomerInput,required=True )

        def mutate(self, info, input):
            created_customers = []
            errors = []

            for index, data in enumerate(input):
                try:
                    if Customer.objects.filter(email=data.email).exists():
                        raise Exception("Email already exists")
                    
                    validate_phone(data.phone)

                    customer = Customer.objects.create(
                        name=data.name,
                        email=data.email,
                        phone=data.phone
                    )

                    created_customers.append(customer)

                except Exception as e:
                    errors.append(f"Row {index +1}: {str(e)}")
            return BulkCreateCustomers(
                customers=created_customers,
                errors=errors
            )


class CreateProduct (graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int()

    def mutate(self, info, name, price, stock=0):
        if price<=0:
            raise Exception("Price must be positive")    
        
        if stock < 0:
            raise Exception("Stock cannot be negative")
        product = Product.objects.create(
            ame=name,
            price=price,
            stock=stock
        )
        return CreateProduct(product=product)
    
class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime()

        @transaction.atomic
        def mutate(self, info, customer_id, product_ids, order_date=None):
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                raise Exception("Invalid customer ID")
            
            if not product_ids:
                raise Exception("At least one product must be selected")
            
            products = Product.objects.filter(id__in=product_ids)

            if products.count() != len(product_ids):
                raise Exception("One or more product ids are invalid ")
            
            total_amount = sum(
                (product.price for product in products),
                Decimal("0.00")
            )
            
            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount,
                order_date=order_date or timezone.now()
            )

            order.products.set(products)

            return CreateOrder(order=order)
        
# -------------------------
# Root Mutation & Query
# -----------------------------
class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customer(root, info):
        return Customer.Objects.all()
    
    def resolve_products(root, info):
        return Product.objects.all()
    
    def resolve_orders(root,  info):
        return Order.objects.all()
    
    class Mutation(graphene.ObjectType):
        create_customer = CreateCustomer.Field()
        bulk_create_customers = BulkCreateCustomers.Field()
        create_product = CreateProduct.Field()
        create_order = CreateOrder.Field()