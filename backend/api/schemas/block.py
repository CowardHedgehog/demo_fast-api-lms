from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class BlockCreate(BaseModel):
  week_id: int
  page: int
  content_id: int
  origin_content_id: int

class BlockRuleCreate(BaseModel):
  block_id: int
  start_date_time: Optional[datetime] = None
  end_date_time: Optional[datetime] = None
  always: Optional[datetime] = True
