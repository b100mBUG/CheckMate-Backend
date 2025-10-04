from backend.database.models import Base
from backend.database.config import engine
import asyncio
async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
if __name__ == "__main__":
    asyncio.run(create_database())