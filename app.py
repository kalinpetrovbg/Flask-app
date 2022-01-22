import random
from datetime import datetime

from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500))
    city = db.Column(db.String(50))
    postcode = db.Column(db.Integer)
    email = db.Column(db.String(200), nullable=False, unique=True)

    orders = db.relationship('Order', backref='customer')


order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    shipped = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    products = db.relationship('Product', secondary=order_product)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True)


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

    for _ in range(1000):
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
        order.prodcuts.extend(purchased)

    db.session.commit()


def create_db():
    db.create_all()
    create_customers()
    create_products()
    create_orders()
    add_order_products()


create_db()


# @app.route('/')
# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__':
    app.run()
