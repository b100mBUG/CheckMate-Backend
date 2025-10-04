from backend.database.config import async_session
from backend.database.models import Company
from sqlalchemy import select
from backend.database.utils import hash_pwd, is_verified_pwd


async def add_company(company_detail: dict):
    async with async_session.begin() as session:
        new_company = Company(
            company_name = company_detail['company_name'],
            company_email = company_detail['company_email'],
            company_contact = company_detail['company_contact'],
            company_password = hash_pwd(company_detail['company_password'])
        )
        try:
            session.add(new_company)
            return new_company
        except Exception as e:
            print("An error occurred: ", e)

async def show_companies(sort_term, sort_dir):
    async with async_session.begin() as session:
        if sort_term == "all":
            stmt = select(Company)
        elif sort_term == "name":
            if sort_dir == "desc":
                stmt = (
                    select(Company)
                    .order_by(Company.company_name.desc())
                )
            elif sort_dir == "asc":
                stmt = (
                    select(Company)
                    .order_by(Company.company_name.asc())
                )
        elif sort_term == "date":
            if sort_dir == "desc":
                stmt = (
                    select(Company)
                    .order_by(Company.date_added.desc())
                )
            elif sort_dir == "asc":
                stmt = (
                    select(Company)
                    .order_by(Company.date_added.asc())
                )
        result = await session.execute(stmt)
        companies = result.scalars().all()
        return companies

async def search_companies(search_term: str):
    async with async_session.begin() as session:
        stmt = select(Company).where(
            Company.company_name.ilike(f"%{search_term}%")
        )
        result = await session.execute(stmt)
        companies = result.scalars().all()
        return companies

async def signin(company_detail: dict):
    async with async_session.begin() as session:
        stmt = select(Company).where(Company.company_name == company_detail['name'])
        result = await session.execute(stmt)
        company = result.scalars().first()
        if not company:
            return None
        if not is_verified_pwd(company.company_password, company_detail['password']):
            return None
        return company

async def delete_company(company_id: int):
    async with async_session.begin() as session:
        stmt = select(Company).where(
            Company.company_id == company_id
        )
        result = await session.execute(stmt)
        company = result.scalars().first()
        if not company:
            return None
        try:
            await session.delete(company)
            await session.commit()
        except Exception as e:
            print("An error occurred: ", e)
            
async def edit_company(company_id: int, company_detail: dict):
    async with async_session.begin() as session:
        stmt = select(Company).where(
            Company.company_id == company_id
        )
        result = await session.execute(stmt)
        company = result.scalars().first()
        if not company:
            return None
        try:
            company.company_name = company_detail['company_name']
            company.company_email = company_detail['company_email']
            company.company_contact = company_detail['company_contact']
            company.company_password = hash_pwd(company_detail['company_password'])
            return company
        except Exception as e:
            print("An error occurred: ", e)
        