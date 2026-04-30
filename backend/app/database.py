import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://projectalpha_user:projectalpha_pass@localhost:5432/projectalpha")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

engine = create_async_engine(DATABASE_URL, echo=DEBUG)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
