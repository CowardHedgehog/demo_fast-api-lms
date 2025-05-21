import asyncio
from api.db import async_engine, Base
from api.migration.add_rows import add_rows
from sqlalchemy.ext.asyncio import AsyncSession
import api.models  # モデルの読み込み（Base.metadataにバインド）

async def reset_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # セッションを使って初期データ挿入
    async with AsyncSession(bind=async_engine) as session:
        await add_rows(session)

if __name__ == "__main__":
    asyncio.run(reset_database())
