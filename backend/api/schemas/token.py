from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
  access_token :str
  token_type: str

class FormData(BaseModel):
  email: str
  password: str
  
class TokenData(BaseModel):
  email: Optional[str] = None
  
class LogoutResponse(BaseModel):
  None