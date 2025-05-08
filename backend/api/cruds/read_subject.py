from fastapi import  Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert, update, func
from typing import List, Optional, Tuple
from jose import JWTError, jwt
from datetime import datetime

from api.db import get_db

import api.models.week as week_model
import api.models.course as course_model
import api.models.subject as subject_model
import api.models.user as user_model
import api.models.block as block_model
import api.models.content as content_model

import api.schemas.week as week_schema
import api.schemas.course as course_schema
import api.schemas.user as user_schema
import api.schemas.subject as subject_schema

import api.cruds.user as user_crud

# コース内の各週（回）情報の取得
async def select_syllabus_info(db: AsyncSession, course_id: int) -> subject_schema.SyllabusInfoResponse:
  result: Result = await(
    db.execute(
      select(
        subject_model.Subject.subject_name,
        subject_model.SubjectInfoSyllabus.subject_id,
        subject_model.SubjectInfoSyllabus.subject_class,
        subject_model.SubjectInfoSyllabus.subject_credit,
        subject_model.SubjectInfoSyllabus.subject_code,
        subject_model.Subject.period.label('subject_period'),
        subject_model.SubjectInfoSyllabus.subject_keyword,
        subject_model.SubjectInfoSyllabus.subject_goals
      ).where(course_model.Course.id == course_id)
      .where(course_model.Course.subject_id == subject_model.Subject.id)
      .where(subject_model.Subject.id == subject_model.SubjectInfoSyllabus.subject_id)
    )
  )
  return result.first()

async def get_syllabus_info(db: AsyncSession, course_id: int):
  return await select_syllabus_info(db=db, course_id=course_id)


async def select_subjects(db: AsyncSession, user: user_schema.User):
  during_result: Result = await(
    db.execute(
      select(
        subject_model.Subject.id,
        subject_model.Subject.subject_name,
        subject_model.Subject.period,
        subject_model.Subject.created,
        user_model.User.username
      ).where(subject_model.Subject.period == "2025年度1期（前学期）")
      .where(subject_model.Subject.created_by == user_model.User.id)
    )
  )
  outside_result: Result = await(
    db.execute(
      select(
        subject_model.Subject.id,
        subject_model.Subject.subject_name,
        subject_model.Subject.period,
        subject_model.Subject.created,
        user_model.User.username
      ).where(subject_model.Subject.period != "2025年度1期（前学期）")
      .where(subject_model.Subject.created_by == user_model.User.id)
    )
  )
  result = {
    'during_result': during_result.mappings().all(),
    'outside_result': outside_result.mappings().all()
  }
  return result

async def get_subjects(db: AsyncSession, user: user_schema.User):
  return await select_subjects(db=db, user=user)
