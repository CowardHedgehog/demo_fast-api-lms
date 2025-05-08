from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import io
from os import isatty
from typing import List,Optional
from urllib import response

import api.cruds.user as user_crud
import api.cruds.read_subject as read_subject_crud

import api.schemas.user as user_schema
import api.schemas.subject as subject_schema

from api.db import get_db

router = APIRouter()

# シラバス情報取得
@router.get('/get_syllabus_info/{course_id}', response_model=subject_schema.SyllabusInfoResponse, tags=['subject'])
async def get_syllabus_info(course_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
  return await read_subject_crud.get_syllabus_info(db, course_id)

# 科目一覧取得
@router.get('/get_subjects', tags=['subject'])
async def get_subjects(user: user_schema.User=Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
  return await read_subject_crud.get_subjects(db, user)