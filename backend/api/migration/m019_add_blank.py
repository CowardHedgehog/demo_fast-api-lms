from sqlalchemy.ext.asyncio import AsyncSession

import api.models.flow_page as flow_page_model
from datetime import datetime
from zoneinfo import ZoneInfo

async def add_blank(db:AsyncSession):
  rows = [
    flow_page_model.Blank(
      id = 1,
      blank_name = 'blank1',
      flowpage_id = 1
    ),
    flow_page_model.Blank(
      id = 2,
      blank_name = 'blank1',
      flowpage_id = 2
    ),
    flow_page_model.Blank(
      id = 3,
      blank_name = 'blank1',
      flowpage_id = 3
    ),
    flow_page_model.Blank(
      id = 4,
      blank_name = 'blank1',
      flowpage_id = 4
    ),
    flow_page_model.Blank(
      id = 5,
      blank_name = 'blank1',
      flowpage_id = 5
    ),
    flow_page_model.Blank(
      id = 6,
      blank_name = 'blank1',
      flowpage_id = 6
    ),
    flow_page_model.Blank(
      id = 7,
      blank_name = 'blank1',
      flowpage_id = 7
    ),
    flow_page_model.Blank(
      id = 8,
      blank_name = 'blank2',
      flowpage_id = 7
    ),
    flow_page_model.Blank(
      id = 9,
      blank_name = 'blank1',
      flowpage_id = 8
    ),
    flow_page_model.Blank(
      id = 10,
      blank_name = 'blank1',
      flowpage_id = 9
    )
  ]
  db.add_all(rows)
  await db.flush()