from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import io
from os import isatty
from typing import List,Optional
from urllib import response

import api.cruds.user as user_crud
import api.cruds.flow as flow_crud
import api.cruds.update_flowpage as update_flowpage_crud

import api.schemas.user as user_schema
import api.schemas.flow as flow_schema
import api.schemas.flow_page as flow_page_schema

from api.db import get_db

router = APIRouter()

# フロー情報取得
@router.get('/get_flow/{flow_id}', response_model=flow_schema.FlowResponse, tags=['flow'])
async def get_flow(flow_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    is_readalbe = await flow_crud.is_readable_flow(db, flow_id, user) ## 未実装 flowの閲覧権限関係
    if not is_readalbe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.get_flow(db, flow_id)

@router.get("/get_flow_welcome_page/{flow_id}", response_model=flow_schema.ContentResponse, tags=['flow'])
async def get_flow(flow_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    is_readalbe = await flow_crud.is_readable_flow(db, flow_id, user)
    if not is_readalbe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.get_flow_welcome_page(db, flow_id)

@router.get("/get_flow_completion_page/{flow_id}", response_model=flow_schema.ContentResponse, tags=['flow'])
async def get_flow(flow_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    is_readalbe = await flow_crud.is_readable_flow(db, flow_id, user)
    if not is_readalbe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.get_flow_completion_page(db, flow_id)

@router.get("/get_flow_sessions/{flow_id}", response_model=List[flow_schema.FlowSessionResponse], tags=['flow'])
async def get_flow_sessions(flow_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_sessions(db, flow_id, user.id)

@router.get('/get_flow_info/{flow_session_id}', response_model=flow_schema.FlowInfoResponse, tags=['flow'])
async def get_flow_info(flow_session_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_info(db, flow_session_id)

@router.get('/get_flowpage/{flow_session_id}/{page}', tags=['flow'])
async def get_flowpage(flow_session_id: int, page: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_session_flowpage(db, flow_session_id, page)

@router.get('/get_flowpage_hint/{flow_session_id}/{page}', tags=['flow'])
async def get_flow_session_flowpage_hint(flow_session_id: int, page: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_session_flowpage_hint(db, flow_session_id, page)

@router.get('/get_blank_answer/{flow_session_id}/{page}', response_model=List[flow_page_schema.BlankAnswerResponse], tags=['flow'])
async def get_blank_answer(flow_session_id: int, page: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_session_flowpage_answer(db, flow_session_id, page)

@router.get('/get_flow_session_history/{course_id}', tags=['flow'])
async def get_flow_session_history(course_id: int, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.get_flow_session_history(db, user.id, course_id)

@router.get('/get_week_flows/{week_id}', response_model=List[flow_schema.WeekFlowsResponse], tags=['flow'])
async def get_week_flows(week_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.get_week_flows(db, week_id)

@router.get('/get_flow_session_student_score/{course_id}', tags = ['flow'])
async def get_flow_session_student_score(course_id: int, user:user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession = Depends(get_db)):
    return await flow_crud.get_flow_session_student_score(db, user.id, course_id)

@router.get('/get_flow_session_teacher_score/{course_id}', tags = ['flow'])
async def get_flow_session_teacher_score(course_id: int, user:user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession = Depends(get_db)):
    return await flow_crud.get_flow_session_teacher_score(db, course_id)

@router.get('/get_week_flowpage/{week_id}', tags=['test'])
async def get_week_flowpage(week_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession = Depends(get_db)):
    return await flow_crud.get_week_flowpage(db, week_id)
    







@router.post("/start_new_flow_session", response_model=flow_schema.StartFlowSessionResponse, tags=['flow'])
async def start_new_flow_session(start_flow_session_request: flow_schema.StartFlowSessionRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    is_startable = await flow_crud.is_startable_flow_session(db, start_flow_session_request.flow_id, user.id)
    if not is_startable:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await flow_crud.start_new_flow_session(db, start_flow_session_request.flow_id, user.id)
  
@router.post("/finish_flow_session", response_model=flow_schema.FinishFlowSessionResponse, tags=['flow'])
async def finish_flow_session(finish_flow_session_request: flow_schema.FinishFlowSessionRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.finish_flow_session(db, user.id, finish_flow_session_request.flow_session_id)
  
@router.post("/register_blank_answer", response_model=List[flow_schema.RegisterAnswerResponse], tags=['flow'])
async def register_blank_answer(answer_blank_request: List[flow_page_schema.AnswerBlankRequest], user: user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await flow_crud.register_blank_answer(db, answer_blank_request)

@router.post("/update_question", tags=['test'])
async def update_question_content(update_question_request: flow_page_schema.UpdateQuestionRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.update_question(db, user, update_question_request)

@router.post("/update_choices", tags=['test'])
async def update_choices_content(update_choices_request: flow_page_schema.UpdateChoicesRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.update_choices(db, user, update_choices_request)

@router.post("/update_flowpage_content", tags=['update_flowpage'])
async def update_flowpage_content(update_flowpage_request: flow_page_schema.UpdateFlowPageRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await update_flowpage_crud.update_flowpage(db, user, update_flowpage_request)

@router.post("/flow", tags=['flow'])
async def register_flow(flow: flow_schema.RegisterFlowRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.register_flow(db, flow)

@router.post("/group", tags=['flow'])
async def register_group(group: flow_schema.RegisterGroupRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.register_group(db, group)

@router.post("/flowpage", tags=['flow'])
async def register_flowpage(flowpage: flow_schema.RegisterFlowPageRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.register_flowpage(db, flowpage)






@router.put("/flow", tags=['flow'])
async def update_flow(flow: flow_schema.UpdateFlowRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.update_flow(db, flow)

@router.put("/group", tags=['flow'])
async def update_group(group: flow_schema.UpdateGroupRequest, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.update_group(db, group)