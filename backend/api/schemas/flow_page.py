from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

class BlankCreate(BaseModel):
    blank_name: str
    flowpage_id: int

class CorrectAnswerCreate(BaseModel):
    blank_id: int
    type: str
    value: str

# 拡張用の基底クラス
class FlowPageCreate(BaseModel):
    title: str
    page_type: str
    page_group: int
    order: int
    content_id: int
    hint_comment_id: int
    answer_comment_id: int
    origin_content_id: int
    origin_hint_comment_id: int
    origin_answer_comment_id: int

class PageCreate(FlowPageCreate):
    page_type: str = "Page"

# 拡張用の基底クラス
class QuestionCreate(FlowPageCreate):
    page_type: str = "Question"

class SingleTextQuestionCreate(QuestionCreate):
    page_type: str = "SingleTextQuestion"

class MultipleTextQuestionCreate(QuestionCreate):
    page_type: str = "MultipleTextQuestion"
    answer_column_content_id: int
    origin_answer_column_content_id: int

class DescriptiveTextQuestionCreate(QuestionCreate):
    page_type: str = "DescriptiveTextQuestion"

class ChoiceQuestionCreate(QuestionCreate):
    page_type: str = "ChoiceQuestion"

class ChoiceQuestionChoicesCreate(BaseModel):
    id: str
    flowpage_id: int
    order: int
    content_id: int

# Response用
class ChoiceQuestionChoiceResponse(BaseModel):
    id: str
    content: str
    order: int

class FlowPageContentResponse(BaseModel):
    content: str

class PageResponse(FlowPageContentResponse):
    pass

class QuestionResponse(FlowPageContentResponse):
    pass

class SingleTextQuestionResponse(FlowPageContentResponse):
    blank_id: str

class MultipleTextQuestionResponse(FlowPageContentResponse):
    answer_column_content: str

class DescriptiveTextQuestionResponse(FlowPageContentResponse):
    blank_id: str

class ChoiceQuestionResponse(FlowPageContentResponse):
    choices : List[ChoiceQuestionChoiceResponse]
    blank_id: str

class FlowpageResponse(BaseModel):
    title: str
    page_type: str
    page_content: FlowPageContentResponse

class BlankAnswerResponse(BaseModel):
    blank_id: int
    answer: str

class FlowpageIncorrectResponse(BaseModel):
    course_id: int
    id: int
    flow_session_id: int
    flowpage_id: int
    content: str

#flowpageの点数を受け取るためのレスポンス
class FlowIscorrectResponse(BaseModel):
    # flow_id
    id: int
    user_id: int
    flowpage_id: int
    is_correct: bool

# Request
class AnswerBlankRequest(BaseModel):
    flow_session_id: int
    page: int
    blank_id: int
    answer: str

# DBに問題の難易度を登録するためのスキーマ
class ItemDifficultyCreate(BaseModel):
    course_id: int
    flow_id: int
    flowpage_id: int
    content_id: int
    difficulty: float
    
# course_id,flow_idから難易度を取得するレスポンス
class QuestionDifficultyResponse(BaseModel):
    flowpage_id: int
    content_id: int
    difficulty: float
    
class UpdateQuestionRequest(BaseModel):
    week_id: int
    content_id: int
    origin_content_id: int
    content: str
  
class Choice(BaseModel):
    id: str
    order: int
    content: str
  
class UpdateChoicesRequest(BaseModel):
    week_id: int
    flowpage_id: int
    choice: List[Choice]
  
class ContentIdList(BaseModel):
    origin_content_id: int
    content_id: int
    origin_hint_comment_id: int
    hint_comment_id: int
    origin_answer_comment_id: int
    answer_comment_id: int
  
class UpdateFlowPageRequest(BaseModel):
    flowpage_id: int
    title: str
    page_type: str
    id_list: ContentIdList
    content: str
    hint_comment: str
    answer_comment: str
    