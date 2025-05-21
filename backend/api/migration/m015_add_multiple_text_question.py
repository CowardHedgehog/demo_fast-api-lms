from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from zoneinfo import ZoneInfo

import api.models.flow_page as flow_page_model

async def add_multiple_text_question(db:AsyncSession):
  rows = [
    flow_page_model.MultipleTextQuestion(
      id = 7,
      title = "Q2-1",
      created = datetime.now(),
      page_type = "multiple_text_question",
      page_group = 3,
      order = 1,
      content_id = 13,
      hint_comment_id = 5,
      answer_comment_id = 6,
      answer_column_content_id = 14,
      origin_content_id = 13,
      origin_hint_comment_id = 5,
      origin_answer_comment_id = 6,
      origin_answer_column_content_id = 14
    )
  ]
  db.add_all(rows)
  await db.flush()
        