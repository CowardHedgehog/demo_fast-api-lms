from fastapi import  Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert, update, delete
from typing import List, Optional, Tuple
from jose import JWTError, jwt
import re
import datetime
from zoneinfo import ZoneInfo

from api.db import get_db

import api.models.course as course_model
import api.models.subject as subject_model
import api.models.user as user_model
import api.models.content as content_model
import api.models.flow as flow_model
import api.models.image as image_model

import api.schemas.course as course_schema
import api.schemas.user as user_schema

import api.cruds.user as user_crud

async def insert_taking_course_student(db: AsyncSession, user: user_schema.User, register_taking_course_request: course_schema.RegisterTakingCourseRequest) -> course_schema.RegisterTakingCourseResponse:
  error_msg = ''
  success = True
  for user_id in register_taking_course_request.user_list:
    user_result: Result = await(
      db.execute(
        select(
          user_model.User.username,
          user_model.User.user_kind_id
        ).where(user_model.User.id == user_id)
      )
    )
    user_info = user_result.mappings().first()
    if user_info == None:
      error_msg += f'{user_id}のユーザが見つかりませんでした．\n'
      success = False
    if user_info['user_kind_id'] == 1 or user_info['user_kind_id'] == 2:
      error_msg += f'{user_id}のユーザ種別が異なります．\n'
      success = False
    taking_course_result: Result = await(
      db.execute(
        select(
          course_model.TakingCourse.user_id,
          course_model.TakingCourse.course_id
        ).where(course_model.TakingCourse.user_id == user_id)
        .where(course_model.TakingCourse.course_id == register_taking_course_request.course_id)
      )
    )
    if taking_course_result.first() != None:
      error_msg += f'{user_id}はすでにこのコースを履修中です．\n'
      success = False
  if success == True:
    try:
      for user_id in register_taking_course_request.user_list:
        row = course_model.TakingCourse(course_id = register_taking_course_request.course_id, user_id = user_id)
        db.add(row)
        await db.flush()
      await db.commit()
      return {'success': True}
    except:
      db.rollback()
      return {'success': False, 'error_msg': 'エラーが発生しました．もう一度選択し直してください．'}
  else:
    return {'success': False, 'error_msg': error_msg}

async def insert_grant_course_teacher(db: AsyncSession, user: user_schema.User, register_grant_course_request: course_schema.RegisterGrantCourseRequest) -> course_schema.RegisterGrantCourseResponse:
  error_msg = ''
  success = True
  for user in register_grant_course_request.user_list:
    user_result : Result = await(
      db.execute(
        select(
          user_model.User.username,
          user_model.User.user_kind_id
        ).where(user_model.User.id == user.id)
      )
    )
    user_info = user_result.mappings().first()
    if user_info == None:
      error_msg += f'{user.username}のユーザが見つかりませんでした．\n'
      success = False
    if user_info['user_kind_id'] != 2:
      error_msg += f'{user.username}のユーザ種別が異なります．\n'
      success = False
  if success == True:
    try:
      for user in register_grant_course_request.user_list:
        row = course_model.CourseGrant(user_id=user.id, course_id=register_grant_course_request.course_id, start_date_time=datetime.datetime.now(), end_date_time=datetime.datetime.now() + datetime.timedelta(days=365), read_answer=user.read_answer, update_answer=user.update_answer, delete_answer=user.delete_answer)
        db.add(row)
        await db.flush()
      await db.commit()
      return {'success': True}
    except:
      db.rollback()
      return {'success': False, 'error': 'エラーが発生しました．もう一度選択し直してください．'}
  else:
    return {'success': False, 'error_msg': error_msg}
  
async def insert_course(db: AsyncSession, user: user_schema.User, register_course_request: course_schema.RegisterCourseRequest):
  row = course_model.Course(
    subject_id = register_course_request.subject_id,
    course_name = register_course_request.course_name,
    weeks = register_course_request.weeks,
    start_date_time = register_course_request.start_date_time,
    end_date_time = register_course_request.end_date_time,
    created = datetime.datetime.now(ZoneInfo("Asia/Tokyo")),
    created_by = user.id,
    is_active = True
  )
  db.add(row)
  await db.flush()
  await db.commit()
  return {'success': True}
  
  
  
  
  
  

async def update_grant_course_teacher(db: AsyncSession, user: user_schema.User, register_grant_course_request: course_schema.RegisterGrantCourseRequest):
  for user in register_grant_course_request.user_list:
    print(user)
    if not user.read_answer and not user.update_answer and not user.delete_answer:
      delete_result: Result = await(
        db.execute(
          delete(course_model.CourseGrant)
          .where(course_model.CourseGrant.course_id == register_grant_course_request.course_id)
          .where(course_model.CourseGrant.user_id == user.id)
        )
      )
    else:
      update_result: Result = await(
        db.execute(
          update(course_model.CourseGrant)
          .where(course_model.CourseGrant.course_id == register_grant_course_request.course_id)
          .where(course_model.CourseGrant.user_id == user.id)
          .values(
            read_answer = user.read_answer, 
            update_answer = user.update_answer,
            delete_answer = user.delete_answer
          )
        )
      )
  await db.commit()
  return {'result': True}

async def update_course_info(db: AsyncSession, user: user_schema.User, update_course_request: course_schema.UpdateCourseRequest):
  update_result: Result = await(
    db.execute(
      update(course_model.Course)
      .where(course_model.Course.id == update_course_request.course_id)
      .values(
        course_name = update_course_request.course_name,
        start_date_time = update_course_request.start_date_time,
        end_date_time = update_course_request.end_date_time,
        weeks = update_course_request.weeks
      )
    )
  )
  await db.commit()
  return {'success': True}











async def delete_taking_course_student(db: AsyncSession, user: user_schema.User, delete_taking_course_request: course_schema.RegisterTakingCourseRequest):
  for user_id in delete_taking_course_request.user_list:
    delete_result: Result = await(
      db.execute(
        delete(course_model.TakingCourse)
        .where(course_model.TakingCourse.course_id == delete_taking_course_request.course_id)
        .where(course_model.TakingCourse.user_id == user_id)
      )
    )
  await db.commit()
  return {'success': True}

async def delete_course_content(db: AsyncSession, user: user_schema.User, delete_course_request: course_schema.DeleteCourseRequest):
  delete_result: Result = await(
    db.execute(
      update(course_model.Course)
      .where(course_model.Course.id == delete_course_request.course_id)
      .values(
        is_active = False
      )
    )
  )
  await db.commit()
  return {'success': True}



# 学生のコース登録
async def register_taking_student(db: AsyncSession, user: user_schema.User, register_taking_course_request: course_schema.RegisterTakingCourseRequest):
  register_taking_course_response = await insert_taking_course_student(db=db, register_taking_course_request=register_taking_course_request, user=user)
  return register_taking_course_response

# 学生のコース削除
async def delete_taking_student(db: AsyncSession, user: user_schema.User, delete_taking_course_request: course_schema.RegisterTakingCourseRequest):
  delete_taking_course_response = await delete_taking_course_student(db=db, delete_taking_course_request=delete_taking_course_request, user=user)
  return delete_taking_course_response

# 教師の権限登録
async def register_grant_teacher(db: AsyncSession, user: user_schema.User, register_grant_course_request: course_schema.RegisterGrantCourseRequest):
  register_grant_course_response = await insert_grant_course_teacher(db=db, register_grant_course_request=register_grant_course_request, user=user)
  return register_grant_course_response

# 教師の権限更新
async def update_grant_teacher(db: AsyncSession, user: user_schema.User, register_grant_course_request: course_schema.RegisterGrantCourseRequest):
  update_grant_course_response = await update_grant_course_teacher(db=db, register_grant_course_request=register_grant_course_request, user=user)
  return update_grant_course_response

# コース登録
async def create_course(db: AsyncSession, user: user_schema.User, register_course_request: course_schema.RegisterCourseRequest):
  register_course_response = await insert_course(db=db, register_course_request=register_course_request, user=user)
  return register_course_response

# コース情報更新
async def update_course(db: AsyncSession, user: user_schema.User, update_course_request: course_schema.UpdateCourseRequest):
  update_course_response = await update_course_info(db=db, update_course_request=update_course_request, user=user)
  return update_course_response

# コース削除（非表示）
async def delete_course(db: AsyncSession, user: user_schema.User, delete_course_request: course_schema.DeleteCourseRequest):
  delete_course_response = await delete_course_content(db=db, delete_course_request=delete_course_request, user=user)
  return delete_course_response