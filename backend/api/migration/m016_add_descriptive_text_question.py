from sqlalchemy.ext.asyncio import AsyncSession

import api.models.flow_page as flow_page_model
from datetime import datetime
from zoneinfo import ZoneInfo

def add_descriptive_text_question(db:AsyncSession):
  rows = [
    flow_page_model.DescriptiveTextQuestion(
      id = 8,
      title = 'Q2-2',
      created = datetime.now(ZoneInfo('Asia/Tokyo')),
      page_type = "descriptive_text_question",
      page_group = 3,
      order = 2,
      content_id = 15,
      hint_comment_id = 5,
      answer_comment_id = 6,
      origin_content_id = 15,
      origin_hint_comment_id = 5,
      origin_answer_comment_id = 6,
    )
  ]
  for row in rows:
    db.add(row)
  db.flush()