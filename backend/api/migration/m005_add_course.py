from sqlalchemy.ext.asyncio import AsyncSession
import api.models.course as course_model
import datetime

def add_course(db: AsyncSession):
  rows = [
    course_model.Course(
      id = 1,
      subject_id = 1,
      course_name = 'Sample Course1',
      weeks = 1,
      start_date_time = datetime.datetime(2024, 4, 1, 0, 0, 0),
      end_date_time = datetime.datetime(2025, 4, 1, 0, 0, 0),
      created = datetime.datetime(2024, 4, 1, 0, 0, 0),
      created_by = 2,
      is_active = True
    )
  ]
  for row in rows:
    db.add(row)
  db.flush()