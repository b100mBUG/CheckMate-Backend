from sqlalchemy import (
    Integer, Text, String,
    Date, Column, ForeignKey,
    Float
)
from sqlalchemy.ext.declarative import declarative_base
from backend.database.utils import current_date
from sqlalchemy.orm import relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False, index=True)
    company_email = Column(String, index=True)
    company_contact = Column(String)
    company_password = Column(String)
    date_added = Column(Date, default=current_date)
    
    accounts = relationship("Account", back_populates="company", cascade="all, delete-orphan")
    salesmen = relationship("Salesman", back_populates="company", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="company", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="company", cascade="all, delete-orphan")
    
class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    account_name = Column(String, nullable=False, index=True)
    account_email = Column(String, index = True)
    account_contact = Column(String)
    account_type = Column(String)
    account_password = Column(String)
    date_added = Column(Date, default=current_date)
    
    company = relationship("Company", back_populates="accounts")

class Salesman(Base):
    __tablename__ = "salesmen"
    salesman_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    salesman_name = Column(String, nullable=False, index=True)
    salesman_email = Column(String, index=True)
    salesman_contact = Column(String)
    salesman_password = Column(String)
    salesman_status = Column(String, default="active")
    salesman_target = Column(Float, default=10000)
    date_added = Column(Date, default=current_date)
    
    company = relationship("Company", back_populates="salesmen")
    orders = relationship("Order", back_populates="salesman", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    salesman_id = Column(Integer, ForeignKey("salesmen.salesman_id"))
    order_name = Column(String, index=True)
    order_detail = Column(Text)
    order_quantity = Column(Integer, default=0)
    
    customer_name = Column(String, nullable=False, index=True)
    customer_email = Column(String, index=True)
    customer_contact = Column(String)
    
    longitude = Column(Float)
    latitude = Column(Float)
    order_status = Column(String, default="pending")
    date_added = Column(Date, default=current_date)
    
    company = relationship("Company", back_populates="orders")
    salesman = relationship("Salesman", back_populates="orders")

class Product(Base):
    __tablename__ = "order_products"
    product_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    product_name = Column(String, index=True, unique=True)
    product_category = Column(String, index=True)
    product_description = Column(Text)
    product_price = Column(Float, default = 0.0)
    product_quantity = Column(Integer, default = 0)
    date_added = Column(Date, default=current_date)
    
    company = relationship("Company", back_populates="products")
    
