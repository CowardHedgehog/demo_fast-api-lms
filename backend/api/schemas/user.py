from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class User(BaseModel):
  id: int
  username: str
  email: str
  hashed_password: str
  created: datetime
  is_active: bool
  user_kind_id: int

class HomeUserProfile(BaseModel):
  username: str
  email: str
  kind_name: str
  create: bool
  is_active: bool

class TakingUsersResponse(BaseModel):
  id: int
  username: str
  email: str
  kind_name: str
  
class TakingResponse(BaseModel):
  registered: List[TakingUsersResponse]
  unregistered: List[TakingUsersResponse]
  
class UserWithGrant(BaseModel):
  id:int
  username: str
  email: str
  created: datetime
  is_active: bool
  kind_name: str
  create: bool
  
  # 推定したユーザの能力値を登録するスキーマ
class UserAbilityCreate(BaseModel):
  week_id: int
  flow_id: int
  username: str
  user_id: int
  ability: float

class UserAbilityResponse(BaseModel):
  ability: float
    
class UpdatePasswordRequest(BaseModel):
  email: str
  old_password: str
  new_password: str
  
class UpdatePasswordResponse(BaseModel):
  success: bool
  email: str
  error_msg: str
  password: str
  
class AddUserRequest(BaseModel):
  username: str
  email: str
  password: str
  kind_name: str

class UserCreate(BaseModel):
  username: str
  email: str
  hashed_password: str
  user_kind_id: int
  created: datetime

class AddUser(BaseModel):
  id: int
  username: str
  email: str
  created: datetime
  is_active: bool
  kind_name: str

class AddUsersResponse(BaseModel):
  success: bool
  error_msg: str
  added_users: Optional[List[AddUser]] = None
  
  
class AddAccessHistoryRequest(BaseModel):
  date: date
  time: int
  page: str
  details: str = ""

class AddAccessHistory(BaseModel):
  user_id: int
  date: date
  time: int
  page: str
  details:str

class GoalRequest(BaseModel):
  details: str

class GoalResponse(GoalRequest):
  pass

class ToggleRequest(BaseModel):
  goal_id : int
  completed : bool

class ThemeRequest(BaseModel):
  theme: str

class PointRequest(BaseModel):
  point:int

class GoalDeleteRequest(BaseModel):
  goal_id: int

class SetNicknameRequest(BaseModel):
  nickname:str