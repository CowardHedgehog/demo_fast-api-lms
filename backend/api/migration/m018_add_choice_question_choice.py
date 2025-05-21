from sqlalchemy.ext.asyncio import AsyncSession
import datetime

import api.models.flow_page as flow_page_model

async def add_choice_question_choice(db:AsyncSession):
  rows = [
    flow_page_model.ChoiceQuestionChoice(
      id = "choice_1",
      flowpage_id = 9,
      order = 1,
      content_id = 17
    ),
    flow_page_model.ChoiceQuestionChoice(
      id = "choice_2",
      flowpage_id = 9,
      order = 2,
      content_id = 18
    ),
    flow_page_model.ChoiceQuestionChoice(
      id = "choice_3",
      flowpage_id = 9,
      order = 3,
      content_id = 19
    ),
    flow_page_model.ChoiceQuestionChoice(
      id = "choice_4",
      flowpage_id = 9,
      order = 4,
      content_id = 20
    ),
  ]
  db.add_all(rows)
  await db.flush()
      