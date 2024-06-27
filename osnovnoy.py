import uuid
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
from database import *

app = FastAPI()


@app.get('/products')
def get_products():
    with Session(autoflush=False, bind=engine) as db:
        products = db.query(Product).all()
        response = []
        for i in products:
            response.append({
                'code': i.code,
                'name': i.name,
                'price': i.price
            })
        result = {'products': response}
        return result

@app.get('/customers')
def get_customers():
    with Session(autoflush=False, bind=engine) as db:
        customers = db.query(Order).all()
        response = []
        for i in customers:
            response.append({
                'name': i.customer_name,
                'address': i.customer_address,
                'phone': i.customer_phone,
                'order_code': i.code
            })
        result = {'customers': response}
        return result

@app.get('/orders_by_date')
def get_orders_by_date():
    with Session(autoflush=False, bind=engine) as db:
        orders = db.query(Order.contract_date, func.count(Order.code)).group_by(Order.contract_date).all()
        response = []
        for i in orders:
            response.append({
                'contract_date': i[0],
                'order_count': i[1]
            })
        result = {'orders_by_date': response}
        return result

@app.get('/shipments/{date}')
def get_shipments(date: str):
    with Session(autoflush=False, bind=engine) as db:
        shipments = db.query(Shipment).filter(Shipment.shipment_date == date).all()
        response = []
        for i in shipments:
            response.append({
                'shipment_date': i.shipment_date,
                'shipped_quantity': i.shipped_quantity
            })
        result = {'shipments': response}
        return result

@app.get('/orders_gt_100')
def get_orders_gt_100():
    with Session(autoflush=False, bind=engine) as db:
        orders = db.query(Order).filter(Order.planned_delivery > 100).all()
        response = []
        for i in orders:
            response.append({
                'order_code': i.code,
                'planned_delivery': i.planned_delivery
            })
        result = {'orders': response}
        return result

@app.get('/customers_by_period/{start_date}/{end_date}')
def get_customers_by_period(start_date: str, end_date: str):
    with Session(autoflush=False, bind=engine) as db:
        customers = db.query(Order).filter(Order.contract_date.between(start_date, end_date)).all()
        response = []
        for i in customers:
            response.append({
                'customer_name': i.customer_name,
                'contract_date': i.contract_date
            })
        result = {'customers': response}
        return result

@app.get('/products_gt_5000')
def get_products_gt_5000():
    with Session(autoflush=False, bind=engine) as db:
        products = db.query(Product).filter(Product.price > 5000).all()
        response = []
        for i in products:
            response.append({
                'product_code': i.code,
                'price': i.price
            })
        result = {'products': response}
        return result

@app.get('/orders_by_word/{word}')
def get_orders_by_word(word: str):
    with Session(autoflush=False, bind=engine) as db:
        orders = db.query(Order).filter(Order.contract_number.contains(word)).all()
        response = []
        for i in orders:
            response.append({
                'order_code': i.code,
                'contract_number': i.contract_number
            })
        result = {'orders': response}
        return result

@app.get('/customer_orders_total/{customer_name}')
def get_customer_orders_total(customer_name: str):
    with Session(autoflush=False, bind=engine) as db:
        subquery = db.query(Order.product_code, Order.planned_delivery, Product.price).join(Product).filter(Order.customer_name == customer_name).subquery()
        total = db.query(func.sum(subquery.c.planned_delivery * subquery.c.price)).group_by(subquery.c.product_code).all()
        response = []
        for i in total:
            response.append({
                'total': i[0]
            })
        result = {'total': response}
        return result

@app.get('/products_gt_1000')
def get_products_gt_1000():
    with Session(autoflush=False, bind=engine) as db:
        products = db.query(Order).filter(Order.planned_delivery > 1000).all()
        response = []
        for i in products:
            response.append({
                'product_code': i.product_code,
                'planned_delivery': i.planned_delivery
            })
        result = {'products': response}
        return result

@app.get('/shipments_by_order/{order_code}')
def get_shipments_by_order(order_code: int):
    with Session(autoflush=False, bind=engine) as db:
        shipments = db.query(Shipment).filter(Shipment.order_code == order_code).all()
        response = []
        for i in shipments:
            response.append({
                'shipment_code': i.code,
                'shipped_quantity': i.shipped_quantity
            })
        result = {'shipments': response}
        return result

@app.get('/customers_by_shipped_quantity/{quantity}')
def get_customers_by_shipped_quantity(quantity: int):
    with Session(autoflush=False, bind=engine) as db:
        subquery = db.query(Shipment.order_code, Shipment.shipped_quantity).subquery()
        customers = db.query(Order).join(subquery, Order.code == subquery.c.order_code).filter(subquery.c.shipped_quantity == quantity).all()
        response = []
        for i in customers:
            response.append({
                'customer_name': i.customer_name,
                'shipped_quantity': quantity
            })
        result = {'customers': response}
        return result

@app.get('/products_by_action')
def get_products_by_action():
    with Session(autoflush=False, bind=engine) as db:
        products = db.query(Order).filter(Order.planned_delivery.contains("акция")).all()
        response = []
        for i in products:
            response.append({
                'product_code': i.product_code,
                'planned_delivery': i.planned_delivery
            })
        result = {'products': response}
        return result

@app.get('/orders_le_50')
def get_orders_le_50():
    with Session(autoflush=False, bind=engine) as db:
        orders = db.query(Order).filter(Order.planned_delivery <= 50).all()
        response = []
        for i in orders:
            response.append({
                'order_code': i.code,
                'planned_delivery': i.planned_delivery
            })
        result = {'orders': response}
        return result

@app.get('/order_shipped_total/{order_code}')
def get_order_shipped_total(order_code: int):
    with Session(autoflush=False, bind=engine) as db:
        subquery = db.query(Shipment.order_code, Shipment.shipped_quantity, Product.price).join(Product).filter(Shipment.order_code == order_code).subquery()
        total = db.query(func.sum(subquery.c.shipped_quantity * subquery.c.price)).first()
        response = []
        response.append({
            'total': total[0]
        })
        result = {'total': response}
        return result

@app.get('/products_gt_avg')
def get_products_gt_avg():
    with Session(autoflush=False, bind=engine) as db:
        subquery = db.query(func.avg(Product.price)).scalar_subquery()
        products = db.query(Product).filter(Product.price > subquery).all()
        response = []
        for i in products:
            response.append({
                'product_code': i.code,
                'price': i.price
            })
        result = {'products': response}
        return result

@app.get('/orders_gt_value/{value}')
def get_orders_gt_value(value: int):
    with Session(autoflush=False, bind=engine) as db:
        orders = db.query(Order).filter(Order.planned_delivery > value).all()
        response = []
        for i in orders:
            response.append({
                'order_code': i.code,
                'planned_delivery': i.planned_delivery
            })
        result = {'orders': response}
        return result

@app.get('/orders_by_range/{start_date}/{end_date}')
def get_orders_by_range(start_date: str, end_date: str):
    with Session(autoflush=False, bind=engine) as db:
        orders = db.query(Shipment).filter(Shipment.shipment_date.between(start_date, end_date)).all()
        response = []
        for i in orders:
            response.append({
                'order_code': i.order_code,
                'shipment_date': i.shipment_date
            })
        result = {'orders': response}
        return result

@app.get('/update_price/{new_price}')
def update_price(new_price: float):
    with Session(autoflush=False, bind=engine) as db:
        products = db.query(Product).filter(~Product.shipments.any()).all()
        for i in products:
            i.price = new_price
        db.commit()
        return {'message': 'Prices updated successfully'}

@app.get('/customers_with_unfulfilled_orders')
def get_customers_with_unfulfilled_orders():
    with Session(autoflush=False, bind=engine) as db:
        subquery = db.query(Order.customer_name).filter(~Order.shipments.any()).subquery()
        customers = db.query(Customer).filter(Customer.name.in_(subquery)).all()
        response = []
        for i in customers:
            response.append({
                'customer_name': i.name
            })
        result = {'customers': response}
        return result