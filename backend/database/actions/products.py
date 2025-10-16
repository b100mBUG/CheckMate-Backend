from backend.database.config import async_session
from backend.database.models import Product
from sqlalchemy import select
from datetime import datetime
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

async def add_product(product_detail: dict):
    async with async_session.begin() as session:
        new_product = Product(
            company_id = product_detail['company_id'],
            product_name = product_detail['product_name'],
            product_category = product_detail['product_category'],
            product_description = product_detail['product_description'],
            product_price = product_detail['product_price'],
            product_quantity = product_detail['product_quantity']
        )
        try:
            session.add(new_product)
            return new_product
        except Exception as e:
            print(f"An error occurred: {e}")

async def show_products(company_id: int, filter_term: str, filter_dir: str):
    async with async_session.begin() as session:
        stmt = None
        if filter_term == "all":
            stmt = select(Product).where(
                Product.company_id == company_id
            )
        elif filter_term == "name":
            if filter_dir == "desc":
                stmt = (
                    select(Product)
                    .where(Product.company_id == company_id)
                    .order_by(Product.product_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Product)
                    .where(Product.company_id == company_id)
                    .order_by(Product.product_name.asc())
                )
        elif filter_term == "date":
            if filter_dir == "desc":
                stmt = (
                    select(Product)
                    .where(Product.company_id == company_id)
                    .order_by(Product.date_added.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Product)
                    .where(Product.company_id == company_id)
                    .order_by(Product.date_added.asc())
                )
        elif filter_term == "category":
            if filter_dir == "desc":
                stmt = (
                    select(Product)
                    .where(Product.company_id == company_id)
                    .order_by(Product.product_category.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Product)
                    .where(Product.company_id == company_id)
                    .order_by(Product.product_category.asc())
                )
        elif filter_term == "depleted":
            if filter_dir == "desc":
                stmt = (
                    select(Product)
                    .where(
                        (Product.company_id == company_id) &
                        (Product.product_quantity <= 0)
                    )
                    .order_by(Product.product_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Product)
                    .where(
                        (Product.company_id == company_id) &
                        (Product.product_quantity <= 0)
                    )
                    .order_by(Product.product_name.asc())
                )
        elif filter_term == "available":
            if filter_dir == "desc":
                stmt = (
                    select(Product)
                    .where(
                        (Product.company_id == company_id) &
                        (Product.product_quantity >= 1)
                    )
                    .order_by(Product.product_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Product)
                    .where(
                        (Product.company_id == company_id) &
                        (Product.product_quantity >= 1)
                    )
                    .order_by(Product.product_name.asc())
                )
        result = await session.execute(stmt)
        products = result.scalars().all()
        if not products:
            return None
        return products

async def get_product_by_order(company_id: int, order_name: str):
    async with async_session.begin() as session:
        stmt = select(Product).where(
            (Product.company_id == company_id) &
            (Product.product_name == order_name)
        )
        result = await session.execute(stmt)
        product = result.scalars().first()
        if not product:
            return None
        return product

async def search_products(company_id: int, search_term: str):
    async with async_session.begin() as session:
        stmt = select(Product).where(
            (Product.company_id == company_id) &
            (Product.product_name.ilike(f"%{search_term}%"))
        )
        result = await session.execute(stmt)
        products = result.scalars().all()
        if not products:
            return None
        return products


async def edit_products(company_id: int, product_id: int, product_details: dict):
    async with async_session.begin() as session:
        stmt = select(Product).where(
            (Product.company_id == company_id) &
            (Product.product_id == product_id)
        )
        result = await session.execute(stmt)
        product = result.scalars().first()
        if not product: 
            return None
        try:
            product.product_name = product_details['product_name']
            product.product_category = product_details['product_category']
            product.product_description = product_details['product_description']
            product.product_quantity = product_details['product_quantity']
            product.product_price = product_details['product_price']

            await session.refresh(product)
            return product
        except Exception as e:
            print(f"An error occurred: {e}")

async def delete_product(company_id: int, product_id: int):
    async with async_session.begin() as session:
        stmt = select(Product).where(
            (Product.company_id == company_id)&
            (Product.product_id == product_id)
        )
        result = await session.execute(stmt)
        product = result.scalars().first()
        if not product:
            return None
        await session.delete(product)