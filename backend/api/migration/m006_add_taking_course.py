from sqlalchemy.ext.asyncio import AsyncSession
import api.models.course as course_model

def add_taking_course(db: AsyncSession):
  rows = [
    course_model.TakingCourse(
      user_id = 3,
      course_id = 1,
    ),
  ]
  for row in rows:
    db.add(row)
  db.flush()