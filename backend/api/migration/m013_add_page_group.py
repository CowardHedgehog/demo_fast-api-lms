from sqlalchemy.ext.asyncio import AsyncSession

import api.models.page_group as page_group_model
from datetime import datetime

async def add_page_group(db:AsyncSession):
  rows = [
    page_group_model.PageGroup(
      id = 1,
      group_name = 'q1_1',
      flow_id = 1,
      order = 1
    ),
    page_group_model.PageGroup(
      id = 2,
      group_name = 'q1_2',
      flow_id = 1,
      order = 1
    ),
    page_group_model.PageGroup(
      id = 3,
      group_name = 'q2',
      flow_id = 1,
      order = 2
    ),
    page_group_model.PageGroup(
      id = 4,
      group_name = 'q3',
      flow_id = 1,
      order = 3
    )
  ]
  db.add_all(rows)
  await db.flush()