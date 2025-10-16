from backend.database.config import async_session
from backend.database.models import Order, Salesman, Product
from sqlalchemy import select
from datetime import date

async def add_order(order_detail: dict):
    async with async_session.begin() as session:
        new_order = Order(
            salesman_id = order_detail['salesman_id'],
            company_id = order_detail['company_id'],
            order_name = order_detail['order_name'],
            order_detail = order_detail['order_detail'],
            order_quantity = order_detail['order_quantity'],
            customer_name = order_detail['customer_name'],
            customer_email = order_detail['customer_email'],
            customer_contact = order_detail['customer_contact'],
            longitude = order_detail['longitude'],
            latitude = order_detail['latitude'],
        )
        try:
            session.add(new_order)
            return new_order
        except Exception as e:
            print("An error occurred: ", e)

async def show_orders(company_id: int, filter_term: str, filter_dir: str):
    async with async_session.begin() as session:
        if filter_term == "all":
            stmt = (
                select(Order)
                .join(Salesman)
                .where(
                    Salesman.company_id == company_id
                )
            )
        elif filter_term == "salesman":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Salesman.salesman_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Salesman.salesman_name.asc())
                )
        elif filter_term == "customer":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Order.customer_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Order.customer_name.asc())
                )
        elif filter_term == "date":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Order.date_added.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Order.date_added.asc())
                )
        elif filter_term == "pending":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(
                        (Order.order_status == "pending") &
                        (Salesman.company_id == company_id)
                    )
                    .order_by(Order.order_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .joint(Salesman)
                    .where(
                        (Order.order_status == "pending") &
                        (Salesman.company_id == company_id)
                    )
                    .order_by(Order.order_name.asc())
                )
        elif filter_term == "cleared":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(
                        (Order.order_status == "cleared") &
                        (Salesman.company_id == company_id)
                    )
                    .order_by(Order.order_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .join(Salesman)
                    .where(
                        (Order.order_status == "cleared") &
                        (Salesman.company_id == company_id)
                    )
                    .order_by(Order.order_name.asc())
                )
        else:
            return
        result = await session.execute(stmt)
        orders = result.scalars().all()
        return orders
    
async def get_salesman_specific_orders(salesman_id: int, filter_term: str, filter_dir: str):
    async with async_session.begin() as session:
        if filter_term == "all":
            stmt = select(Order).where(
                Order.salesman_id == salesman_id
            )

        elif filter_term == "customer":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .where(Order.salesman_id == salesman_id)
                    .order_by(Order.customer_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .where(Order.salesman_id == salesman_id)
                    .order_by(Order.customer_name.asc())
                )
        elif filter_term == "date":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .where(Order.salesman_id == salesman_id)
                    .order_by(Order.date_added.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .where(Order.salesman_id == salesman_id)
                    .order_by(Order.date_added.asc())
                )
        elif filter_term == "pending":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .where(
                        (Order.order_status == "pending") &
                        (Order.salesman_id == salesman_id)
                    )
                    .order_by(Order.order_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .where(
                        (Order.order_status == "pending") &
                        (Order.salesman_id == salesman_id)
                    )
                    .order_by(Order.order_name.asc())
                )
        elif filter_term == "cleared":
            if filter_dir == "desc":
                stmt = (
                    select(Order)
                    .where(
                        (Order.order_status == "cleared") &
                        (Order.salesman_id == salesman_id)
                    )
                    .order_by(Order.order_name.desc())
                )
            elif filter_dir == "asc":
                stmt = (
                    select(Order)
                    .where(
                        (Order.order_status == "cleared") &
                        (Order.salesman_id == salesman_id)
                    )
                    .order_by(Order.order_name.asc())
                )
        else:
            return
        result = await session.execute(stmt)
        orders = result.scalars().all()
        return orders

async def get_order_by_id(order_id: int):
    async with async_session.begin() as session:
        stmt = select(Order).where(
            Order.order_id == order_id
        )
        result = await session.execute(stmt)
        order = result.scalars().first()
        if not order:
            return None
        return order

async def search_orders(company_id: int, search_by: str, search_term: str):
    async with async_session.begin() as session:
        if search_by == "all":
            stmt = select(Order).where(
                Order.company_id == company_id
            )
        elif search_by == "order":
            stmt = select(Order).where(
                (Order.order_name.ilike(f"%{search_term}%")) &
                (Order.company_id == company_id)
            )
        elif search_by == "salesman":
            stmt = (
                select(Order)
                .join(Salesman)
                .where(
                    (Salesman.salesman_name.ilike(f"%{search_term}%")) &
                    (Order.company_id == company_id)
                )
            )
        elif search_by == "customer":
            stmt = select(Order).where(
                (Order.customer_name.ilike(f"%{search_term}%")) &
                (Order.company_id == company_id)
            )
        result = await session.execute(stmt)
        orders = result.scalars().all()
        return orders

async def search_salesman_orders(salesman_id: int, search_by: str, search_term: str):
    async with async_session.begin() as session:
        stmt = None
        if search_by == "all":
            stmt = select(Order).where(
                Order.salesman_id == salesman_id
            )
        elif search_by == "order":
            stmt = select(Order).where(
                (Order.order_name.ilike(f"%{search_term}%")) &
                (Order.salesman_id == salesman_id)
            )
        elif search_by == "salesman":
            stmt = (
                select(Order)
                .join(Salesman)
                .where(
                    (Order.order_name.ilike(f"%{search_term}%")) &
                    (Order.salesman_id == salesman_id)
                )
            )
        elif search_by == "customer":
            stmt = select(Order).where(
                (Order.customer_name.ilike(f"%{search_term}%")) &
                (Order.salesman_id == salesman_id)
            )
        result = await session.execute(stmt)
        orders = result.scalars().all()
        return orders

async def date_span_orders_filter(company_id: int, start_date: date, end_date: date):
    async with async_session.begin() as session:
        stmt = select(Order).where(
            (Order.company_id == company_id) &
            (Order.date_added >= start_date) &
            (Order.date_added <= end_date)
        )
        result = await session.execute(stmt)
        orders = result.scalars().all()
        return orders or None

async def delete_order(order_id: int):
    async with async_session.begin() as session:
        stmt = select(Order).where(
            Order.order_id == order_id
        )
        result = await session.execute(stmt)
        order = result.scalars().first()
        if not order:
            return None
        try:
            await session.delete(order)
        except Exception as e:
            print("An error occurred: ", e)
            
async def clear_order(order_id: int):
    async with async_session.begin() as session:
        stmt = select(Order).where(
            Order.order_id == order_id
        )
        result = await session.execute(stmt)
        order = result.scalars().first()
        if not order:
            return None
        prod_stmt = select(Product).where(
            (Product.company_id == order.company_id) &
            (Product.product_name == order.order_name)
        )
        prod_result = await session.execute(prod_stmt)
        product = prod_result.scalars().first()
        if not product:
            return None
        try:
            if product.product_quantity < order.order_quantity:
                return None
            product.product_quantity -= order.order_quantity
            order.order_status = "cleared"
            return order
        except Exception as e:
            print("An error occurred: ", e)

async def edit_order(order_id: int, order_detail: dict):
    async with async_session.begin() as session:
        stmt = select(Order).where(
            Order.order_id == order_id
        )
        result = await session.execute(stmt)
        order = result.scalars().first()
        if not order:
            return None
        try:
            order.order_name = order_detail['order_name']
            order.order_detail = order_detail['order_detail']
            order.order_quantity = order_detail['order_quantity']
            order.customer_email = order_detail['customer_email']
            order.customer_contact = order_detail['customer_contact']
            return order
        except Exception as e:
            print("An error occurred: ", e)
