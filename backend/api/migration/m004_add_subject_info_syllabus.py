from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.subject as subject_model

def add_subject_info_syllabus(db: AsyncSession):
  rows = [
    subject_model.SubjectInfoSyllabus(
      subject_id = 1,
      subject_class = '授業科目区分',
      subject_credit = 0,
      subject_code = 'X000-00',
      subject_keyword = 'キーワード1,キーワード2,キーワード3,キーワード4,キーワード5',
      subject_goals = '学習・教育目標'
    )
  ]
  for row in rows:
    db.add(row)
  db.flush()
  