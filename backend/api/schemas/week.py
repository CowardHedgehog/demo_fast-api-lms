from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class WeekResponse(BaseModel):
  week_id: int
  week_name: str
  week_num: int
  order: int
  
# Weekコンテンツ登録時
class WeekFiles(BaseModel):
  file_path: str
  file_text: str

class RegisterWeekRequest(BaseModel):
  week_name: str                # Weekコンテンツ名
  week_num: int                 # 第〇回、第〇週
  order: int                    # 第〇回、第〇週内での並び順
  course_id: int                # 対応するCourse_id
  week_files: List[WeekFiles]   # 登録するweekファイル

# Week登録時のレスポンス
class RegisteredWeek(BaseModel):
  id: int
  course_id: int
  week_name: str
  week_num: int
  order: int
  created: datetime

class RegisterWeekResponse(BaseModel):
  success: bool
  error_msg: str
  registered_week: Optional[RegisteredWeek] = None
  
class WeekCreate(BaseModel):
  course_id: int
  week_name: str
  week_num: int
  order: int
  created_by: int
  
class UpdateWeekContentRequest(BaseModel):
  course_id: int
  week_id: int
  content_id: int
  origin_content_id: int
  content: str

class UpdateWeekRequest(BaseModel):
  week_id: int
  week_name: str
  week_num: int
  order: int

class UpdateWeekResponse(BaseModel):
  success: bool
  
class DeleteWeekRequest(BaseModel):
  week_id: int
  
class DeleteWeekResponse(BaseModel):
  success: bool