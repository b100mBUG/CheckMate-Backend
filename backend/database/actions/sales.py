from backend.database.models import Salesman, Product, Order
from backend.database.config import async_session
from sqlalchemy import select
from datetime import datetime, timedelta

async def generate_total_sales(company_id: int, filter: str) -> list[dict]:
    async with async_session() as session: 
        stmt = stmt = select(Order).where(
            (Order.company_id == company_id) &
            (Order.order_status == "cleared")
        )
        today = datetime.today().date()
        if filter == "all":
            stmt = stmt
        elif filter == "this month":
            month_ago = today - timedelta(days=30)
            stmt = stmt.where(Order.date_added >= month_ago)
        
        elif filter == "last month":
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            stmt = stmt.where(
                (Order.date_added >= first_day_last_month) &
                (Order.date_added <= last_day_last_month)
            )
            
        result = await session.execute(stmt)
        cleared_orders = result.scalars().all()

        if not cleared_orders:
            return []

        order_sales = []

        for order in cleared_orders:
            product_stmt = select(Product).where(
                (Product.company_id == order.company_id) &
                (Product.product_name == order.order_name)
            )
            product_result = await session.execute(product_stmt)
            sold_product = product_result.scalars().first()

            if not sold_product:
                continue

            total_sales_per_order = sold_product.product_price * order.order_quantity
            order_sales.append({
                "order_id": order.order_id,
                "product_name": order.order_name,
                "quantity": order.order_quantity,
                "price": sold_product.product_price,
                "total_sales": total_sales_per_order
            })

        return order_sales

async def generate_salesman_sales(company_id: int, salesman_id: int, filter: str) -> list[dict]:
    async with async_session() as session:
        today = datetime.today().date()
        stmt = select(Order).where(
            (Order.company_id == company_id) &
            (Order.order_status == "cleared") &
            (Order.salesman_id == salesman_id)
        )

        if filter == "month":
            month_ago = today - timedelta(days=30)
            stmt = stmt.where(Order.date_added >= month_ago)

        result = await session.execute(stmt)
        cleared_orders = result.scalars().all()

        if not cleared_orders:
            return []

        salesman_stmt = select(Salesman).where(Salesman.salesman_id == salesman_id)
        salesman_result = await session.execute(salesman_stmt)
        salesman = salesman_result.scalars().first()

        if not salesman:
            return []

        order_sales = []
        for order in cleared_orders:
            product_stmt = select(Product.product_price).where(
                (Product.company_id == order.company_id) &
                (Product.product_name == order.order_name)
            )
            product_result = await session.execute(product_stmt)
            product_price = product_result.scalar()

            if not product_price:
                continue

            total_sales_per_order = product_price * order.order_quantity
            deficit = salesman.salesman_target - total_sales_per_order
            target_percentage = (deficit / salesman.salesman_target) * 100 if salesman.salesman_target else 0

            order_sales.append({
                "order_id": order.order_id,
                "product_name": order.order_name,
                "quantity": order.order_quantity,
                "price": product_price,
                "total_sales": total_sales_per_order,
                "target": salesman.salesman_target,
                "target_deficit": deficit,
                "target_percentage": target_percentage
            })

        return order_sales
