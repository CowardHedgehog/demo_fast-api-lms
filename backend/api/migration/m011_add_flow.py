from sqlalchemy.ext.asyncio import AsyncSession

import api.models.flow as flow_model
from datetime import datetime

def add_flow(db:AsyncSession):
  rows = [
    flow_model.Flow(
      id = 1, 
      id_in_yml = "week1_1", 
      week_id = 1,
      title = "演習問題1", 
      created = datetime(2024,4,1,0,0,0),
      welcome_page_content_id = 3,
      completion_page_content_id = 4,
    ),
    flow_model.Flow(
      id = 2, 
      id_in_yml = "week1_2", 
      week_id = 1,
      title = "演習問題2", 
      created = datetime(2024,4,1,0,0,0),
      welcome_page_content_id = 3,
      completion_page_content_id = 4,
    )
  ]
  for row in rows:
    db.add(row)
  db.flush()