from sqlalchemy.ext.asyncio import AsyncSession

import api.models.block as block_model

def add_block(db:AsyncSession):
  rows = [
    block_model.Block(
      id = 1,
      week_id = 1,
      page = 1,
      content_id = 1,
      origin_content_id = 1
    ),
    block_model.Block(
      id = 2,
      week_id = 1,
      page = 2,
      content_id = 2,
      origin_content_id = 2
    ),
  ]
  for row in rows:
    db.add(row)
  db.flush()