from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from zoneinfo import ZoneInfo

from api.cruds.domains.generate_hash import get_password_hash
import api.models.user as user_model

async def add_user(db: AsyncSession):
  administrators = [
    user_model.User(
      id = 1,
      username = 'admin',
      email = 'admin@user.com',
      hashed_password = get_password_hash('admin'),
      user_kind_id = 1,
      created = datetime.now(),
      is_active = True
    ),
  ]
  teachers = [
    user_model.User(
      id = 2, 
      username = "teach",
      email = "teach@user.com",
      hashed_password = get_password_hash("teach"),
      user_kind_id = 2,
      created = datetime.now(),
      is_active = True
    ),
  ]
  students = [
    user_model.User(
      id = 3, 
      username = "stud",
      email = "stud@user.com",
      hashed_password = get_password_hash("stud"),
      user_kind_id = 3,
      created = datetime.now(),
      is_active = True
    ),
  ]
  test_users = [
    user_model.User(
      id = 4,
      username = "test",
      email = "test@user.com",
      hashed_password = get_password_hash("test"),
      user_kind_id = 4,
      created = datetime.now(),
      is_active = True
    ),
  ]
  db.add_all(administrators)
  db.add_all(teachers)
  db.add_all(students)
  db.add_all(test_users)
  await db.flush()