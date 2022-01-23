from db_models import Order, Customer, Product, order_product
from db_models import db


def get_orders_by(customer_id):
    print(f'Get orders by customer: {Customer.query.filter_by(id=customer_id).first().name}')
    customer_orders = Order.query.filter_by(customer_id=customer_id).all()
    for order in customer_orders:
        print(order.id)


# get_orders_by(22)

def get_all_delivered_orders():
    print(f'Get list with all delivered orders:')
    delivered_orders = Order.query.filter(Order.shipped.__eq__(1)).all()
    print([x.id for x in delivered_orders])


# get_all_delivered_orders()


def find_clients_from_the_same_city(client_id):
    client = Customer.query.filter_by(id=client_id).first()
    city = Customer.query.filter(Customer.city.is_(client.city)).all()  # isnot as well
    print([x.name for x in city])


# find_clients_from_the_same_city(2)


def get_all_customers_alphabetically():
    all_customers = Customer.query.order_by(Customer.name.asc()).all()
    print([x.name for x in all_customers])


# get_all_customers_alphabetically()


def how_many_orders():
    print(Order.query.count())


# how_many_orders()


def get_all_customers_starting_with_a():
    all_customers = Customer.query.order_by(Customer.name.asc()).filter(Customer.name.startswith('A')).all()
    print([x.name for x in all_customers])


# get_all_customers_starting_with_a()


def get_all_customers_who_spent_more(amount):
    customers = db.session.query(Customer) \
        .join(Order) \
        .join(order_product) \
        .join(Product).group_by(Customer).having(db.func.sum(Product.price) > amount).all()

    for customer in customers:
        print(customer.name)

    print(len(customers))


# get_all_customers_who_spent_more(5000)


def update_values():
    old_data = Order.query.filter_by(shipped=1).all()
    print(len(old_data))
    updated = Order.query.filter_by(shipped=1).update({Order.shipped: 0})
    print(updated)
    db.session.commit()

    # check results
    old_data = Order.query.filter_by(shipped=1).all()
    print(len(old_data))


# update_values()


def limit_only_two_customers():
    customers = Customer.query.limit(2).all()
    print(customers)


# limit_only_two_customers()


def get_num_of_orders_per_client():
    result = db.session.query(Customer.name, db.func.count(Order.customer_id)) \
        .outerjoin(Order, Customer.id == Order.customer_id) \
        .group_by(Customer.name).all()
    print(result)

# get_num_of_orders_per_client()


def get_sum_of_orders_per_client():
    # but not having a column Order.price
    result = db.session.query(Customer.name, db.func.sum(Order.price)) \
        .outerjoin(Order, Customer.id == Order.customer_id) \
        .group_by(Customer.name).all()
    print(result)

# get_sum_of_orders_per_client()
