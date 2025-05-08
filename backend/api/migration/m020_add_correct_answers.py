from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

import api.models.flow_page as flow_page_model

def add_correct_answer(db: AsyncSession):
  rows = [
    flow_page_model.CorrectAnswer(
      id = 1,
      blank_id = 1,
      type = 'str',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 2,
      blank_id = 1,
      type = 'int',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 3,
      blank_id = 2,
      type = 'str',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 4,
      blank_id = 2,
      type = 'int',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 5,
      blank_id = 3,
      type = 'str',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 6,
      blank_id = 3,
      type = 'int',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 7,
      blank_id = 4,
      type = 'str',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 8,
      blank_id = 4,
      type = 'int',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 9,
      blank_id = 5,
      type = 'str',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 10,
      blank_id = 5,
      type = 'int',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 11,
      blank_id = 6,
      type = 'str',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 12,
      blank_id = 6,
      type = 'int',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 13,
      blank_id = 7,
      type = 'str',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 14,
      blank_id = 7,
      type = 'int',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 15,
      blank_id = 8,
      type = 'str',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 16,
      blank_id = 8,
      type = 'int',
      value = 1
    ),
    flow_page_model.CorrectAnswer(
      id = 17,
      blank_id = 9,
      type = 'str',
      value = 'Descriptive'
    ),
    flow_page_model.CorrectAnswer(
      id = 18,
      blank_id = 10,
      type = 'str',
      value = 'choice_1'
    )
  ]
  for row in rows:
    db.add(row)
  db.flush()