from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy import Column, Integer, String, ForeignKey, REAL, Boolean, DateTime
from sqlalchemy.orm import relationship


DATABASE_URL = 'mysql://isp_p_Bobrenev:12345@77.91.86.135/isp_p_Bobrenev' # измените на соответствующий URL базы данных

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase): ...

class Product(Base):
    __tablename__ = 'products'
    code = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    orders = relationship("Order", back_populates="product")
    shipments = relationship("Shipment", secondary="shipment_product", back_populates="products")

class Order(Base):
    __tablename__ = 'orders'
    code = Column(Integer, primary_key=True)
    customer_name = Column(String)
    customer_address = Column(String)
    customer_phone = Column(String)
    contract_number = Column(String)
    contract_date = Column(Date)
    product_code = Column(Integer, ForeignKey('products.code'))
    planned_delivery = Column(Integer)
    product = relationship("Product", back_populates="orders")

class Shipment(Base):
    __tablename__ = 'shipments'
    code = Column(Integer, primary_key=True)
    order_code = Column(Integer, ForeignKey('orders.code'))
    shipment_date = Column(Date)
    shipped_quantity = Column(Integer)
    products = relationship("Product", secondary="shipment_product", back_populates="shipments")

# Association Table for many-to-many relationship between Product and Shipment
class ShipmentProduct(Base):
    __tablename__ = 'shipment_product'
    shipment_code = Column(Integer, ForeignKey('shipments.code'), primary_key=True)
    product_code = Column(Integer, ForeignKey('products.code'), primary_key=True)



Base.metadata.create_all(engine)

