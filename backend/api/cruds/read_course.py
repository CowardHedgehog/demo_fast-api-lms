from fastapi import  Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert, update
from typing import List, Optional, Tuple
from jose import JWTError, jwt
from datetime import datetime

from api.db import get_db

import api.models.course as course_model
import api.models.subject as subject_model
import api.models.user as user_model

import api.schemas.course as course_schema
import api.schemas.user as user_schema

import api.cruds.user as user_crud

# ユーザが履修中のコースを取得
async def select_taking_course(db: AsyncSession, user_id: int):
  result: Result = await(
    db.execute(
      select(
        course_model.Course.id.label('course_id'),
        course_model.Course.course_name,
        subject_model.Subject.subject_name,
        subject_model.Subject.period
      ).where(course_model.TakingCourse.course_id == course_model.Course.id)
      .where(course_model.Course.subject_id == subject_model.Subject.id)
      .where(user_id == course_model.TakingCourse.user_id)
      .where(course_model.Course.is_active == True)
    )
  )
  return result.all()

# 単一コースの情報を取得
async def select_course_info(db: AsyncSession, user: user_schema.User, course_id: int):
  course_result: Result = await(
    db.execute(
      select(
        subject_model.Subject.subject_name,
        course_model.Course.course_name,
        subject_model.Subject.period,
        course_model.Course.weeks,
        course_model.Course.start_date_time,
        course_model.Course.end_date_time
      ).where(course_id == course_model.Course.id)
      .where(course_model.Course.subject_id == subject_model.Subject.id)
    )
  )
  result = course_result.mappings().first()
  if user.created:
    grant_result: Result = await(
      db.execute(
        select(
          course_model.CourseGrant.read_answer,
          course_model.CourseGrant.update_answer,
          course_model.CourseGrant.delete_answer
        ).where(user.id == course_model.CourseGrant.user_id)
        .where(course_model.CourseGrant.course_id == course_id)
      )
    )
    grant = grant_result.mappings().first()
    if user.user_kind_id == 1:
      grant = {"read_answer": True, "update_answer": True, "delete_answer": True}
    if grant != None:
      result = {**result, **grant}
    print(result, grant)
  return result

# 作成・共有中コースを取得
async def select_created_courses(db: AsyncSession, user_id: int, kind_id: int, subject_id: int):# -> course_schema.TakingCourseResponse:
  create_result: Result = await(
    db.execute(
      select(
        course_model.Course.id.label('course_id'),
        course_model.Course.course_name,
        subject_model.Subject.subject_name,
        subject_model.Subject.period,
        user_model.User.username
      ).where(subject_id == subject_model.Subject.id)
      .where(course_model.Course.subject_id == subject_model.Subject.id)
      .where(user_id == course_model.Course.created_by)
      .where(course_model.Course.is_active == True)
      .where(course_model.Course.created_by == user_model.User.id)
    )
  )
  if kind_id != 1:
    share_result: Result = await(
      db.execute(
        select(
          course_model.Course.id.label('course_id'),
          subject_model.Subject.subject_name,
          course_model.Course.course_name,
          subject_model.Subject.period,
          user_model.User.username,
          course_model.CourseGrant.read_answer,
          course_model.CourseGrant.update_answer,
          course_model.CourseGrant.delete_answer
        ).where(subject_id == subject_model.Subject.id)
        .where(subject_model.Subject.id == course_model.Course.subject_id)
        .where(course_model.Course.id == course_model.CourseGrant.course_id)
        .where(course_model.CourseGrant.user_id == user_id)
        .where(user_model.User.id == course_model.Course.created_by)
        .where(course_model.Course.is_active == True)
      )
    )
  
  else: # 管理者はすべてのコースを表示できるようにするため
    share_result: Result = await(
      db.execute(
        select(
          course_model.Course.id.label('course_id'),
          subject_model.Subject.subject_name,
          course_model.Course.course_name,
          subject_model.Subject.period,
          user_model.User.username,
        ).where(subject_id == subject_model.Subject.id)
        .where(subject_model.Subject.id == course_model.Course.subject_id)
        .where(user_model.User.id == course_model.Course.created_by)
        .where(user_id != course_model.Course.created_by)
        .where(course_model.Course.is_active == True)
      )
    )
  
  result = {
    'created': create_result.mappings().all(),
    'shared': share_result.mappings().all()
  }
  return result

# 共有されているコース一覧を取得
async def select_grant_courses(db: AsyncSession, user_id: int):
  result: Result = await(
    db.execute(
      select(
        subject_model.Subject.subject_name,
        course_model.Course.course_name,
        subject_model.Subject.period,
        user_model.User.username,
        course_model.CourseGrant.read_answer,
        course_model.CourseGrant.update_answer,
        course_model.CourseGrant.delete_answer
      ).where(subject_model.Subject.id == course_model.Course.subject_id)
      .where(course_model.Course.id == course_model.CourseGrant.course_id)
      .where(course_model.CourseGrant.user_id == user_id)
      .where(user_model.User.id == course_model.Course.created_by)
    )
  )
  return result.mappings().all()

async def select_taking_students(db: AsyncSession, course_id: int) -> user_schema.TakingResponse:
  registered_student_result :Result = await(
    db.execute(
      select(
        user_model.User.id,
        user_model.User.username,
        user_model.User.email,
        user_model.UserKind.kind_name
      ).where(user_model.User.user_kind_id == user_model.UserKind.id)
      .where(course_model.TakingCourse.user_id == user_model.User.id)
      .where(course_id == course_model.TakingCourse.course_id)
    )
  )
  registered = registered_student_result.mappings().all()
  unregistered_student_result :Result = await(
    db.execute(
      select(
        user_model.User.id,
        user_model.User.username,
        user_model.User.email,
        user_model.UserKind.kind_name
      ).where(user_model.User.user_kind_id == user_model.UserKind.id)
      .where((user_model.UserKind.kind_name == '学生') | (user_model.UserKind.kind_name == 'テスト'))
      .where(user_model.User.id.notin_(
        select(
          user_model.User.id
        ).where(course_model.TakingCourse.user_id == user_model.User.id)
        .where(course_id == course_model.TakingCourse.course_id)
      ))
    )
  )
  unregistered = unregistered_student_result.mappings().all()
  result = {
    'registered': registered,
    'unregistered': unregistered
  }
  return result

async def select_grant_teachers(db: AsyncSession, course_id: int):
  registered_teachers_result: Result = await(
    db.execute(
      select(
        user_model.User.id,
        user_model.User.username,
        user_model.User.email,
        course_model.CourseGrant.read_answer,
        course_model.CourseGrant.update_answer,
        course_model.CourseGrant.delete_answer
      ).where(user_model.User.id == course_model.CourseGrant.user_id)
      .where(course_model.CourseGrant.course_id == course_id)
    )
  )
  registered = registered_teachers_result.mappings().all()
  unregistered_teachers_result: Result = await(
    db.execute(
      select(
        user_model.User.id,
        user_model.User.username,
        user_model.User.email,
      ).where(user_model.User.user_kind_id == 2)
      .where(user_model.User.id.notin_(
        select(
          user_model.User.id
        ).where(course_model.CourseGrant.user_id == user_model.User.id)
        .where(course_id == course_model.CourseGrant.course_id)
      ))
    )
  )
  unregistered = unregistered_teachers_result.mappings().all()
  result = {
    'registered': registered,
    'unregistered': unregistered
  }
  return result




# 履修中のコースを取得
async def get_taking_courses(user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession = Depends(get_db)):
  return await select_taking_course(db=db, user_id=user.id)

# コース情報を取得
async def get_course_info(course_id: int, user=user_schema.User, db: AsyncSession = Depends(get_db)):
  return await select_course_info(db=db, user=user, course_id=course_id)

# 作成したコースを取得
async def get_created_courses(subject_id: int, user_id: int, kind_id: int, db: AsyncSession):
  return await select_created_courses(db=db, user_id=user_id, kind_id=kind_id, subject_id=subject_id)

# 共有（権限付与）されているコースを取得
async def get_grant_courses(db: AsyncSession, user_id: int):
  return await select_grant_courses(db=db, user_id=user_id)

async def get_taking_students(db: AsyncSession, course_id: int):
  return await select_taking_students(db=db, course_id=course_id)

async def get_grant_teachers(db: AsyncSession, course_id: int):
  return await select_grant_teachers(db=db, course_id=course_id)


