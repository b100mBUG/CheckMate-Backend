from backend.database.config import async_session
from backend.database.models import Account
from sqlalchemy import select
from backend.database.utils import hash_pwd, is_verified_pwd


async def create_account(account_detail: dict):
    async with async_session.begin() as session:
        new_account = Account(
            account_name = account_detail['account_name'],
            company_id = account_detail['company_id'],
            account_email = account_detail['account_email'],
            account_contact = account_detail['account_contact'],
            account_type = account_detail['account_type'],
            account_password = hash_pwd(account_detail['account_password'])
        )
        try:
            session.add(new_account)
            return new_account
        except Exception as e:
            print("An error occurred: ", e)

async def signin(account_detail: dict):
    async with async_session.begin() as session:
        stmt = select(Account).where(Account.account_name == account_detail['name'])
        result = await session.execute(stmt)
        account = result.scalars().first()
        if not account:
            return None
        if not is_verified_pwd(account.account_password, account_detail['password']):
            return None
        return account

async def show_accounts(sort_term: str, sort_dir: str):
    async with async_session.begin() as session:
        if sort_term == "all":
            stmt = select(Account)
        elif sort_term == "name":
            if sort_dir == "desc":
                stmt = (
                    select(Account)
                    .order_by(Account.account_name.desc())
                )
            elif sort_dir == "asc":
                stmt = (
                    select(Account)
                    .order_by(Account.account_name.asc())
                )
        elif sort_term == "date":
            if sort_dir == "desc":
                stmt = (
                    select(Account)
                    .order_by(Account.date_added.desc())
                )
            if sort_dir == "asc":
                stmt = (
                    select(Account)
                    .order_by(Account.date_added.asc())
                )
        result = await session.execute(stmt)
        accounts = result.scalars().all()
        return accounts

async def search_accounts(search_term: str):
    async with async_session.begin() as session:
        stmt = select(Account).where(
            Account.account_name.ilike(f"%{search_term}%")
        )
        result = await session.execute(stmt)
        accounts = result.scalars().all()
        return accounts

async def delete_account(account_id: int):
    async with async_session.begin() as session:
        stmt = select(Account).where(
            Account.account_id == account_id
        )
        result = await session.execute(stmt)
        account = result.scalars().first()
        if not account:
            return None
        try:
            await session.delete(account)
        except Exception as e:
            print("An error occurred: ", e)

async def edit_account(account_id: int, account_detail: dict):
    async with async_session.begin() as session:
        stmt = select(Account).where(
            Account.account_id == account_id
        )
        result = await session.execute(stmt)
        account = result.scalars().first()
        if not account:
            return None
        try:
            account.account_name = account_detail['account_name']
            account.account_email = account_detail['account_email']
            account.account_contact = account_detail['account_contact']
            account.account_type = account_detail['account_type']
            account.account_password = hash_pwd(account_detail['account_password'])
            return account
        except Exception as e:
            print("An error occurred: ", e)