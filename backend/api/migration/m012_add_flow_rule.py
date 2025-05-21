from sqlalchemy.ext.asyncio import AsyncSession

import api.models.flow as flow_model
from datetime import datetime

async def add_flow_rule(db:AsyncSession):
  rows = [
    flow_model.FlowRule(
      flow_id = 1, 
      check_answer_timing = 'submit_page', 
      restart_session = True,
      always = True
    ),
    flow_model.FlowRule(
      flow_id = 2, 
      check_answer_timing = 'submit_page', 
      restart_session = False,
      always = True
    ),
  ]
  db.add_all(rows)
  await db.flush()