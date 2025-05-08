from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import io
from os import isatty
from typing import List,Optional
from urllib import response

import api.cruds.read_week as read_week_crud
import api.cruds.create_week as create_week_crud
import api.cruds.update_week as update_week_crud
import api.cruds.user as user_crud
import api.cruds.update_week as update_week_crud

import api.schemas.week as week_schema
import api.schemas.user as user_schema

from api.db import get_db
router = APIRouter()

# コース内のWeek情報取得
@router.get('/get_weeks/{course_id}', response_model=List[week_schema.WeekResponse], tags=['read_week'])
async def get_weeks(course_id: int, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await read_week_crud.get_weeks(db, course_id)

@router.get('/get_week/{week_id}', response_model=week_schema.WeekResponse, tags=['read_week'])
async def get_week(week_id: int, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await read_week_crud.get_week(db, week_id)

# コンテンツ取得
@router.get('/get_week_content/{week_id}/{page}', tags=['read_week'])
async def get_week_content(week_id: int, page: int, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await read_week_crud.get_week_content(db, week_id, page)

# 置換前のコンテンツ取得
@router.get('/get_week_origin_content/{course_id}/{week_id}', tags=['read_week'])
async def get_week_origin_content(course_id: int, week_id: int, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await read_week_crud.get_week_origin_content(db, course_id, week_id)


# コンテンツ登録
@router.post("/register_week", response_model=week_schema.RegisterWeekResponse, tags=['register_week'])
async def register_week(register_week_request: week_schema.RegisterWeekRequest, user_grant: user_schema.UserWithGrant=Depends(user_crud.get_user_grant), db: AsyncSession=Depends(get_db)):
  if not user_grant.create:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
  return await create_week_crud.register_week(user_grant,register_week_request,db)

# weekコンテンツの更新
@router.post('/update_week_content', tags=['update_week'])
async def update_week_content(update_week_content_request: week_schema.UpdateWeekContentRequest, user_grant: user_schema.UserWithGrant=Depends(user_crud.get_user_grant), db: AsyncSession=Depends(get_db)):
  if not user_grant.create:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
  return await update_week_crud.update_week_content(db=db, course_id=update_week_content_request.course_id, week_id=update_week_content_request.week_id, content_id=update_week_content_request.content_id, origin_content_id=update_week_content_request.origin_content_id, content=update_week_content_request.content)

# week情報の更新
@router.post('/update_week', tags=['update_week'])
async def update_week(update_week_request: week_schema.UpdateWeekRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_week_crud.update_week(db=db, user=user, update_week_request=update_week_request)

# week情報の削除
@router.post('/delete_week', tags=['update_week'])
async def delete_week(delete_week_request: week_schema.DeleteWeekRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_week_crud.delete_week(db=db, user=user, delete_week_request=delete_week_request)