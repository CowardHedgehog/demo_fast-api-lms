from sqlalchemy.ext.asyncio import AsyncSession
import api.models.week as week_model
from datetime import datetime

async def add_week(db: AsyncSession):
  rows = [
    week_model.Week(
      id = 1,
      course_id = 1,
      week_name = '第1週コンテンツ',
      week_num = 1,
      order = 1,
      created = datetime(2024, 4, 1, 0, 0, 0),
      created_by = 1,
    )
  ]
  db.add_all(rows)
  await db.flush()