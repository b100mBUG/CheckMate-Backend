from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

database_url = "postgresql+asyncpg://fidelcastro:NXFDa7exbwGbUHQ8JrUuVwHTNTvkHtCB@dpg-d37njbjuibrs7396lq00-a.oregon-postgres.render.com/shop_up_database"
engine = create_async_engine(url=database_url, echo=False)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)