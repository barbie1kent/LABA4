from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import Column, Integer, String, ForeignKey, REAL, Boolean, DateTime
from sqlalchemy.orm import relationship


DATABASE_URL = 'mysql://isp_p_Bobrenev:12345@77.91.86.135/isp_p_Bobrenev' # измените на соответствующий URL базы данных

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase): ...

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(50))
    price = Column(Float)

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(50))
    customer_address = Column(String(100))
    customer_phone = Column(String(12))
    contract_number = Column(String(4))
    contract_date = Column(Date)
    planned_quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey('products.id'))

    product = relationship("Product")

class Shipment(Base):
    __tablename__ = 'shipment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    shipment_date = Column(Date)
    shipped_quantity = Column(Integer)
    order_id = Column(Integer, ForeignKey('orders.id'))

    order = relationship("Order")



Base.metadata.create_all(engine)

