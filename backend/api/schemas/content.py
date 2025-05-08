from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class ContentCreate(BaseModel):
    content: str

# コンテンツ更新時のリクエスト
class UpdateContentRequest(BaseModel):
    content_id: int
    course_id: int
    block_id: int
    content: str