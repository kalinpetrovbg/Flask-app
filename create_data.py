import random
from app import db
from db_models import Customer, Order, Product
from faker import Faker

fake = Faker()


def create_customers():
    for _ in range(100):
        new_customer = Customer(
            name=fake.name(),
            address=fake.address(),
            city=fake.city(),
            postcode=fake.postcode(),
            email=fake.email()
        )
        db.session.add(new_customer)
        db.session.commit()


def create_products():
    for _ in range(100):
        new_product = Product(
            name=fake.color_name(),
            price=random.randint(10, 999),
            qty=random.randint(1, 11),
            status=random.choices([True, False], [90, 10])[0]
        )
        db.session.add(new_product)
        db.session.commit()


def create_orders():
    customers = Customer.query.all()

    for _ in range(100):
        customer = random.choice(customers)
        date = fake.date_this_year()
        shipped = random.choices([True, False], [5, 95])[0]
        customer_id = customer.id

        order = Order(
            date=date,
            shipped=shipped,
            customer_id=customer_id)

        db.session.add(order)
        db.session.commit()


def add_order_products():
    orders = Order.query.all()
    products = Product.query.all()

    for order in orders:
        # select random k
        k = random.randint(1, 3)
        # select random products
        purchased = random.sample(products, k)
        order.products.extend(purchased)

    db.session.commit()


def create_db():
    db.create_all()
    create_customers()
    create_products()
    create_orders()
    add_order_products()


try:
    create_db()
    print('Database created successfully')
except Exception:
    print('Error')