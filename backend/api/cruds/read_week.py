from fastapi import  Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert, update, func
from typing import List, Optional, Tuple
from jose import JWTError, jwt
from datetime import datetime

from api.db import get_db

import api.models.block as block_model
import api.models.content as content_model
import api.models.course as course_model
import api.models.flow_page as flow_page_model
import api.models.flow_session as flow_session_model
import api.models.flow as flow_model
import api.models.image as image_model
import api.models.subject as subject_model
import api.models.user as user_model
import api.models.week as week_model

import api.schemas.week as week_schema

# コース内の各週（回）情報の取得
async def select_weeks(db: AsyncSession, course_id: int) -> List[week_schema.WeekResponse]:
  result: Result = await(
    db.execute(
      select(
        week_model.Week.id.label('week_id'),
        week_model.Week.week_name,
        week_model.Week.week_num,
        week_model.Week.order
      ).where(course_id == week_model.Week.course_id)
      .where(week_model.Week.is_active == 1)
      .order_by(week_model.Week.week_num, week_model.Week.order)
    )
  )
  return result.all()

async def select_week(db: AsyncSession, week_id: int):
  result: Result = await(
    db.execute(
      select(
        week_model.Week.id.label('week_id'),
        week_model.Week.week_name,
        week_model.Week.week_num,
        week_model.Week.order
      ).where(week_id == week_model.Week.id)
    )
  )
  return result.mappings().first()



# 指定された週のページのコンテンツを取得
async def select_week_content(db: AsyncSession, week_id: int, page: int):
  week_dict = await select_week(db, week_id)
  block_result: Result = await(
    db.execute(
      select(
        content_model.Content.content
      ).where(week_id == block_model.Block.week_id)
      .where(page == block_model.Block.page)
      .where(block_model.Block.content_id == content_model.Content.id)
    )
  )
  page_result: Result = await(
    db.execute(
      select(
        func.count(block_model.Block.content_id)
      ).group_by(block_model.Block.week_id)
      .where(week_id == block_model.Block.week_id)
    )
  )
  block_dict = block_result.mappings().first()
  page_num = page_result.mappings().first()
  output_dict = {
    'week_id': week_dict['week_id'],
    'week_name': week_dict['week_name'],
    'week_num': week_dict['week_num'],
    'page_num': page_num['count'],
    'content': block_dict['content']
  }
  return output_dict

# 指定された週の置換前のコンテンツを取得
async def select_week_origin_content(db: AsyncSession, course_id: int, week_id: int):
  block_result: Result = await(
    db.execute(
      select(
        block_model.Block.page,
        block_model.Block.content_id,
        block_model.Block.origin_content_id,
        content_model.Content.content,
      ).where(week_id == block_model.Block.week_id)
      .where(block_model.Block.origin_content_id == content_model.Content.id)
      .order_by(block_model.Block.page)
    )
  )
  # imageリスト
  image_result: Result = await(
    db.execute(
      select(
        image_model.Image.id,
        image_model.Image.name
      ).where(week_id == image_model.Image.week_id)
    )
  )
  # flowリスト
  flow_result: Result = await(
    db.execute(
      select(
        flow_model.Flow.id.label('flow_id'),
        flow_model.Flow.week_id,
        flow_model.Flow.id_in_yml,
      ).where(course_id == week_model.Week.course_id)
      .where(week_model.Week.id == flow_model.Flow.week_id)
      .where(week_model.Week.is_active == True)
    )
  )
  # pageリスト
  page_result: Result = await(
    db.execute(
      select(
        week_model.Week.id.label('week_id'),
        week_model.Week.week_num,
        week_model.Week.order,
        block_model.Block.page
      ).where(course_id == week_model.Week.course_id)
      .where(week_model.Week.id == block_model.Block.week_id)
      .order_by(week_model.Week.id, week_model.Week.week_num, week_model.Week.order, block_model.Block.page)
    )
  )
    
  block_dict = block_result.mappings().all()
  image_dict = image_result.mappings().all()
  flow_dict = flow_result.mappings().all()
  page_dict = page_result.mappings().all()
  result = {
    'block': block_dict,
    'image': image_dict,
    'flow': flow_dict,
    'page': page_dict
  }
  return result




async def get_weeks(db: AsyncSession, course_id: int):
  return await select_weeks(db=db, course_id=course_id)

async def get_week(db: AsyncSession, week_id: int):
  return await select_week(db=db, week_id=week_id)

async def get_week_content(db: AsyncSession, week_id: int, page: int):
  return await select_week_content(db=db, week_id=week_id, page=page)

async def get_week_origin_content(db: AsyncSession, course_id: int, week_id: int):
  return await select_week_origin_content(db=db, course_id=course_id, week_id=week_id)
