from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class SyllabusInfoResponse(BaseModel):
  subject_name: str
  subject_id: int
  subject_class: str
  subject_credit: int
  subject_code: str
  subject_period: str
  subject_keyword: str
  subject_goals: str