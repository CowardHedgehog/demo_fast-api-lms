from sqlalchemy.ext.asyncio import AsyncSession

import api.models.flow_page as flow_page_model
from datetime import datetime
from zoneinfo import ZoneInfo

async def add_choice_question(db:AsyncSession):
  rows = [
    flow_page_model.ChoiceQuestion(
      id = 9,
      title = 'Q3',
      created = datetime.now(),
      page_type = "choice_question",
      page_group = 4,
      order = 1,
      content_id = 16,
      hint_comment_id = 5,
      answer_comment_id = 6,
      origin_content_id = 16,
      origin_hint_comment_id = 5,
      origin_answer_comment_id = 6,
    )
  ]
  db.add_all(rows)
  await db.flush()