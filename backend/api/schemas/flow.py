from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# フロー情報
class FlowResponse(BaseModel):
    title: str
    check_answer_timing: str
    challenge_limit: Optional[int]
    restart_session: Optional[bool]
    time_limit: Optional[int]
    start_date_time: Optional[datetime]
    end_answer_date_time: Optional[datetime]
    end_read_date_time: Optional[datetime]
    always: bool
  
class ContentResponse(BaseModel):
    content: str

class FlowSessionResponse(BaseModel):
    id: int
    start_date_time: datetime
    finish_date_time: Optional[datetime]
    is_finished: bool
    flow_session_grade: float
    class Config:
        orm_mode = True
        
class StartFlowSessionResponse(BaseModel):
    start_success: bool
    flow_session_id: Optional[int]
    start_date_time: Optional[datetime]

class ResponsePageGroup(BaseModel):
    id: int
    flow_id: int
    order: int

class StartFlowSessionRequest(BaseModel):
    flow_id: int

class FlowSessionCreate(BaseModel):
    user_id: int
    flow_id: int
    start_date_time: datetime

class FinishFlowSessionResponse(BaseModel):
    finish_success: bool
    finish_date_time: Optional[datetime]

class FinishFlowSessionRequest(BaseModel):
    flow_session_id: int

class RegisterAnswerResponse(BaseModel):
    is_correct: bool
    class Config:
        orm_mode = True

class FlowSessionBlankAnswerCreate(BaseModel):
    flow_session_id: int
    flowpage_id: int
    blank_id: int
    answer: str
    created: datetime

class FlowInfoResponse(BaseModel):
    flow_title: str
    num_of_pages: int
  
class FlowSessionBlankAnswerResponse(BaseModel):
    flowpage_id: int
    blank_id: int
    answer: str
  
class WeekFlowsResponse(BaseModel):
    id: int
    title: str
    check_answer_timing: str
    challenge_limit: Optional[int]
    restart_session: Optional[bool]
    time_limit: Optional[int]
    start_date_time: Optional[datetime]
    end_answer_date_time: Optional[datetime]
    end_read_date_time: Optional[datetime]
    always: bool
  
class FlowCreate(BaseModel):
    id_in_yml: str
    week_id: int
    title: str
    welcome_page_content_id: int
    completion_page_content_id: int
  
class FlowGrantCreate(BaseModel):
    user_id: int
    flow_id: int
    start_date_time: datetime
    end_date_time: datetime
    read_answer: bool
    update_answer: bool
    delete_answer: bool

class FlowRuleCreate(BaseModel):
    flow_id: int
    check_answer_timing: Optional[str] = 'submit_page'
    challenge_limit: Optional[int] = None
    restart_session: Optional[bool] = True
    time_limit: Optional[int] = None
    start_date_time: Optional[datetime] = None
    end_answer_date_time: Optional[datetime] = None
    end_read_date_time: Optional[datetime] = None
    always: Optional[bool] = True

class GroupCreate(BaseModel):
    flow_id: int
    group_name: str
    order: int
    
class RegisterFlowRequest(BaseModel):
    week_id: int
    id_in_yml: str
    title: str
    welcome_page_content: str
    completion_page_content: str
    
class UpdateFlowRequest(BaseModel):
    flow_id: int
    id_in_yml: str
    title: str
    welcome_page_content: str
    completion_page_content: str
    welcome_page_content_id: int
    completion_page_content_id: int

class RegisterGroupRequest(BaseModel):
    flow_id: int
    group_name: str
    order: int

class UpdateGroupRequest(BaseModel):
    group_id: int
    group_name: str
    order: int
    
class RegisterFlowPageRequest(BaseModel):
    week_id: int
    group_id: int
    title: str
    order: int
    page_type: str
    content: str
    hint_comment: str
    answer_comment: str
    correct_answers: List[Dict]
    choices: Optional[Any]
    correct_choices: Optional[Any]
