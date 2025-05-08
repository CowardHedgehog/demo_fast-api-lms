from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.subject as subject_model

def add_subject(db: AsyncSession):
  rows = [
    subject_model.Subject(
      id = 1,
      subject_name = 'サンプル',
      period = '2024年度1期（前学期）',
      created = datetime.datetime(2024, 4, 1, 0, 0, 0),
      created_by = 1,
      is_active = True
    ),
  ]
  for row in rows:
    db.add(row)
  db.flush()