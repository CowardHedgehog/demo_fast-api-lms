from sqlalchemy.ext.asyncio import AsyncSession
import api.models.user as user_model

async def add_user_kind(db: AsyncSession):
  rows = [
    user_model.UserKind(id = 1, kind_name = '管理者', create = True),
    user_model.UserKind(id = 2, kind_name = '教師', create = True),
    user_model.UserKind(id = 3, kind_name = '学生', create = False),
    user_model.UserKind(id = 4, kind_name = 'テスト', create = False)
  ]
  db.add_all(rows)
  await db.flush()