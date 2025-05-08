from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class PageGroupCreate(BaseModel):
  group_name: str
  flow_id: int
  order: int

