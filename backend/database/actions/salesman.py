from backend.database.config import async_session
from backend.database.models import Salesman
from backend.database.utils import hash_pwd, is_verified_pwd
from sqlalchemy import select

async def add_salesman(salesman_detail: dict):
    async with async_session.begin() as session:
        new_salesmam = Salesman(
            company_id = salesman_detail['company_id'],
            salesman_name = salesman_detail['salesman_name'],
            salesman_email = salesman_detail['salesman_email'],
            salesman_contact = salesman_detail['salesman_contact'],
            salesman_password = hash_pwd(salesman_detail['salesman_password'])
        )
        try:
            session.add(new_salesmam)
            return new_salesmam
        except Exception as e:
            print("An error occurred: ", e)

async def signin(salesman_detail: dict):
    async with async_session.begin() as session:
        stmt = select(Salesman).where(Salesman.salesman_name == salesman_detail['name'])
        result = await session.execute(stmt)
        salesman = result.scalars().first()
        if not salesman:
            return None
        if not is_verified_pwd(salesman.salesman_password, salesman_detail['password']):
            return None
        return salesman

async def show_salesmen(company_id: int, sort_term: str, sort_dir: str):
    async with async_session.begin() as session:
        stmt = None
        if sort_term == "all":
            stmt = select(Salesman).where(Salesman.company_id == company_id)
        elif sort_term == "name":
            if sort_dir == "desc":
                stmt = (
                    select(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Salesman.salesman_name.desc())
                )
            elif sort_dir == "asc":
                stmt = (
                    select(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Salesman.salesman_name.asc())
                )
        elif sort_term == "date":
            if sort_dir == "desc":
                stmt = (
                    select(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Salesman.date_added.desc())
                )
            if sort_dir == "asc":
                stmt = (
                    select(Salesman)
                    .where(Salesman.company_id == company_id)
                    .order_by(Salesman.date_added.asc())
                )
        elif sort_term == "active":
            if sort_dir == "desc":
                stmt = (
                    select(Salesman)
                    .where(
                        (Salesman.salesman_status == "active")&
                        (Salesman.company_id == company_id)
                    )
                    .order_by(Salesman.salesman_name.desc())
                )
            elif sort_dir == "asc":
                stmt = (
                    select(Salesman)
                    .where(
                        (Salesman.salesman_status == "active") &
                        (Salesman.company_id == company_id)
                    )
                    .order_by(Salesman.salesman_name.asc())
                )
        elif sort_term == "inactive":
            if sort_dir == "desc":
                stmt = (
                    select(Salesman)
                    .where(
                        (Salesman.salesman_status == "inactive")&
                        (Salesman.company_id == company_id)
                    )
                    .order_by(Salesman.salesman_name.desc())
                )
            elif sort_dir == "asc":
                stmt = (
                    select(Salesman)
                    .where(
                        (Salesman.salesman_status == "inactive")&
                        (Salesman.company_id == company_id)
                    )
                    .order_by(Salesman.salesman_name.asc())
                )
        result = await session.execute(stmt)
        salesmen = result.scalars().all()
        return salesmen

async def search_salesmen(company_id: int, search_term: str):
    async with async_session.begin() as session:
        stmt = select(Salesman).where(
            (Salesman.salesman_name.ilike(f"%{search_term}%")) &
            (Salesman.company_id == company_id)
        )
        result = await session.execute(stmt)
        salesmen = result.scalars().all()
        return salesmen

async def deactivate_salesman(company_id: int, salesman_id: int):
    async with async_session.begin() as session:
        stmt = select(Salesman).where(
            (Salesman.salesman_id == salesman_id) &
            (Salesman.company_id == company_id)
        )
        result = await session.execute(stmt)
        salesman = result.scalars().first()
        if not salesman:
            return None
        try:
            salesman.salesman_status = "inactive"
            return salesman
        except Exception as e:
            print("An error occurred: ", e)

async def activate_salesman(company_id: int, salesman_id: int):
    async with async_session.begin() as session:
        stmt = select(Salesman).where(
            (Salesman.salesman_id == salesman_id)  &
            (Salesman.company_id == company_id)
        )
        result = await session.execute(stmt)
        salesman = result.scalars().first()
        if not salesman:
            return None
        try:
            salesman.salesman_status = "active" 
            return salesman
        except Exception as e:
            print("An error occurred: ", e)

async def delete_salesman(company_id: int, salesman_id: int):
    async with async_session.begin() as session:
        stmt = select(Salesman).where(
            (Salesman.salesman_id == salesman_id)  &
            (Salesman.company_id == company_id)
        )
        result = await session.execute(stmt)
        salesman = result.scalars().first()
        if not salesman:
            return None
        try:
            await session.delete(salesman)
        except Exception as e:
            print("An error occurred: ", e)

async def edit_salesman(company_id: int, salesman_id: int, salesman_detail: dict):
    async with async_session.begin() as session:
        stmt = select(Salesman).where(
            (Salesman.salesman_id == salesman_id) &
            (Salesman.company_id == company_id)
        )
        result = await session.execute(stmt)
        salesman = result.scalars().first()
        if not salesman:
            return None
        try:
            salesman.salesman_name = salesman_detail['salesman_name']
            salesman.salesman_email = salesman_detail['salesman_email']
            salesman.salesman_contact = salesman_detail['salesman_contact']
            salesman.salesman_target = salesman_detail['salesman_target']
            return salesman
        except Exception as e:
            print("An error occurred: ", e)
        
