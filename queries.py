from db_models import Order, Customer, Product

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

get_all_delivered_orders()