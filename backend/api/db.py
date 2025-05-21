from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

DATABASE_URL = os.getenv("NEON_DB_URL")

async_engine = create_async_engine(DATABASE_URL, pool_recycle=1800, pool_pre_ping=True, echo=True, connect_args={"ssl": ssl.create_default_context()})

async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session