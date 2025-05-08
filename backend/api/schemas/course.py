from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# コース一覧を取得するためのレスポンス
class TakingCourseResponse(BaseModel):
  course_id: int
  course_name: str
  subject_name: str
  period: str
  
# コース情報を取得したときのレスポンス
class CourseInfoResponse(BaseModel):
  subject_name: str
  course_name: str
  period: str
  weeks: int
  start_date_time: datetime
  end_date_time: datetime
  read_answer: Optional[bool] = False
  update_answer: Optional[bool] = False
  delete_answer: Optional[bool] = False

# 履修者登録時のリクエスト
class RegisterTakingCourseRequest(BaseModel):
  course_id: int
  user_list: List[int]
  
#履修者登録時のレスポンス
class RegisterTakingCourseResponse(BaseModel):
  success: bool
  error_msg: Optional[str] = None
  
# 権限追加時のユーザ情報
class RegisterGrantCourseUserInfo(BaseModel):
  id: int
  email: str
  username: str
  read_answer: Optional[bool] = False
  update_answer: Optional[bool] = False
  delete_answer: Optional[bool] = False

# 権限登録時のリクエスト
class RegisterGrantCourseRequest(BaseModel):
  course_id: int
  user_list: List[RegisterGrantCourseUserInfo]

# 権限登録時のレスポンス
class RegisterGrantCourseResponse(BaseModel):
  success: bool
  error_msg: Optional[str] = None
  
# コース登録時のリクエスト
class RegisterCourseRequest(BaseModel):
  subject_id: int
  course_name: str
  start_date_time: datetime
  end_date_time: datetime
  weeks: int
  
class RegisterCourseResponse(BaseModel):
  success: bool
  course_id: int
  
# コース更新時のリクエスト
class UpdateCourseRequest(BaseModel):
  course_id: int
  course_name: str
  start_date_time: datetime
  end_date_time: datetime
  weeks: int

class UpdateCourseResponse(BaseModel):
  success: bool
  
class DeleteCourseRequest(BaseModel):
  course_id: int
  
class DeleteCourseResponse(BaseModel):
  success: bool
  
class CourseGrant(BaseModel):
  read_answer: Optional[bool] = False
  update_answer: Optional[bool] = False
  delete_answer: Optional[bool] = False