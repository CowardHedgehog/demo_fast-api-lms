from fastapi import APIRouter, Depends, HTTPException, status, Response, FastAPI
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import io
from os import isatty
from typing import List,Optional
from urllib import response

import api.cruds.read_course as read_course_crud
import api.cruds.update_course as update_course_crud
import api.cruds.user as user_crud

import api.schemas.course as course_schema
import api.schemas.user as user_schema

from api.db import get_db

router = APIRouter()


# 履修中のコース情報取得
@router.get('/get_courses', response_model= List[course_schema.TakingCourseResponse], tags=['student_course'], summary='履修中のコース情報取得')
async def get_taking_course(taking_courses: List[course_schema.TakingCourseResponse] = Depends(read_course_crud.get_taking_courses)):
  """
  学生用の履修中のコース一覧取得

  引数:
  - **User**: ユーザ情報

  戻り値:
  リスト型
  
  """
  return taking_courses

# 作成したコース情報取得
@router.get('/get_created_courses/{subject_id}', tags=['course'])
#@router.get('/get_created_courses/{subject_id}', response_model= List[course_schema.TakingCourseResponse], tags=['course'])
async def get_create_course(subject_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await read_course_crud.get_created_courses(db=db, user_id=user.id, kind_id=user.user_kind_id, subject_id=subject_id)

# 共有（権限付与）されているコース情報取得
@router.get('/get_grant_courses', tags=['course'])
async def get_grant_course(user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await read_course_crud.get_grant_courses(db=db, user_id=user.id)

# 単一コースの情報取得
@router.get('/get_course_info/{course_id}', response_model=course_schema.CourseInfoResponse, tags=['course'])
async def get_course_info(course_id: int, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession = Depends(get_db)):
  return await read_course_crud.get_course_info(course_id=course_id, user=user, db=db)

# 履修登録されている学生ユーザの取得
@router.get('/get_taking_students/{course_id}', response_model=user_schema.TakingResponse, tags=['course'])
async def get_taking_students(course_id: int, user: user_schema.User=Depends(user_crud.get_current_active_user) , db: AsyncSession=Depends(get_db)):
  return await read_course_crud.get_taking_students(db=db, course_id=course_id)

# 履修登録されている学生ユーザの取得
@router.get('/get_grant_teachers/{course_id}', tags=['course'])
async def get_grant_teachers(course_id: int, user: user_schema.User=Depends(user_crud.get_current_active_user) , db: AsyncSession=Depends(get_db)):
  return await read_course_crud.get_grant_teachers(db=db, course_id=course_id)



# 学生ユーザの履修登録
@router.post('/register_taking_student', response_model=course_schema.RegisterTakingCourseResponse, tags=['course'])
async def register_taking_student(register_taking_course_request: course_schema.RegisterTakingCourseRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_course_crud.register_taking_student(db=db, user=user, register_taking_course_request=register_taking_course_request)

# 教師ユーザの権限登録
@router.post('/register_grant_teacher', response_model=course_schema.RegisterGrantCourseResponse, tags=['course'])
async def register_grant_teacher(register_grant_course_request: course_schema.RegisterGrantCourseRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_course_crud.register_grant_teacher(db=db, user=user, register_grant_course_request=register_grant_course_request)

# 教師ユーザの権限更新
@router.post('/update_grant_teacher', tags=['course'])
async def update_grant_teacher(register_grant_course_request: course_schema.RegisterGrantCourseRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_course_crud.update_grant_teacher(db=db, user=user, register_grant_course_request=register_grant_course_request)

# 学生ユーザの履修削除
@router.post('/delete_taking_student', tags=['course'])
async def delete_taking_student(delete_taking_course_request: course_schema.RegisterTakingCourseRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_course_crud.delete_taking_student(db=db, user=user, delete_taking_course_request=delete_taking_course_request)

# コースの登録
@router.post('/create_course', tags=['course'])
async def create_course(register_course_request: course_schema.RegisterCourseRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_course_crud.create_course(db=db, user=user, register_course_request=register_course_request)

# コース情報更新
@router.post('/update_course', tags=['course'])
async def update_course(update_course_request: course_schema.UpdateCourseRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_course_crud.update_course(db=db, user=user, update_course_request=update_course_request)

# コースの削除
@router.post('/delete_course', tags=['course'])
async def delete_course(delete_course_request: course_schema.DeleteCourseRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
  return await update_course_crud.delete_course(db=db, user=user, delete_course_request=delete_course_request)