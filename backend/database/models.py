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
    company_name = Column(String, nullable=False)
    company_email = Column(String)
    company_contact = Column(String)
    company_password = Column(String)
    date_added = Column(Date, default=current_date)
    
    accounts = relationship("Account", back_populates="company")
    salesmen = relationship("Salesman", back_populates="company")
    
class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    account_name = Column(String, nullable=False)
    account_email = Column(String)
    account_contact = Column(String)
    account_type = Column(String)
    account_password = Column(String)
    date_added = Column(Date, default=current_date)
    
    company = relationship("Company", back_populates="accounts")

class Salesman(Base):
    __tablename__ = "salesmen"
    salesman_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    salesman_name = Column(String, nullable=False)
    salesman_email = Column(String)
    salesman_contact = Column(String)
    salesman_password = Column(String)
    salesman_status = Column(String, default="active")
    date_added = Column(Date, default=current_date)
    
    company = relationship("Company", back_populates="salesmen")
    orders = relationship("Order", back_populates="salesman")

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    salesman_id = Column(Integer, ForeignKey("salesmen.salesman_id"))
    order_name = Column(String)
    order_detail = Column(Text)
    order_quantity = Column(Integer, default=0)
    
    customer_name = Column(String, nullable=False)
    customer_email = Column(String)
    customer_contact = Column(String)
    
    longitude = Column(Float)
    latitude = Column(Float)
    order_status = Column(String, default="pending")
    date_added = Column(Date, default=current_date)
    
    salesman = relationship("Salesman", back_populates="orders")
    