from sqlalchemy.ext.asyncio import AsyncSession
import api.models.course as course_model

async def add_taking_course(db: AsyncSession):
  rows = [
    course_model.TakingCourse(
      user_id = 3,
      course_id = 1,
    ),
  ]
  db.add_all(rows)
  await db.flush()