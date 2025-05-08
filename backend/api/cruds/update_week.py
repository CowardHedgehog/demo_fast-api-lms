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
import api.models.flow_page as flowpage_model
import api.models.image as image_model
import api.models.week as week_model
import api.models.block as block_model

import api.schemas.course as course_schema
import api.schemas.user as user_schema
import api.schemas.week as week_schema

import api.cruds.user as user_crud
import api.cruds.image as image_crud

async def update_content(db: AsyncSession, id: int, content: str):
  update_result: Result = await(
    db.execute(
      update(content_model.Content)
      .where(content_model.Content.id == id)
      .values(content = content)
    )
  )
  await db.commit()

async def update_week_content(db: AsyncSession, course_id: int, week_id: int, content_id: int, origin_content_id: int, content: str):
  await update_content(db=db, id=origin_content_id, content=content)
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
  flows = flow_result.all()
  print(flows)
  for flow in flows:
    flow_id, week_id, id_in_yml = flow
    #content = re.sub(f"\(\s*flow/{id_in_yml}\s*\)", f"<div class='box'><p>(Flow/{flow_id})</p></div>", content)
    content = re.sub(rf"\[(.*?)\]\s*\(\s*flow/{id_in_yml}\s*\)", rf"<div class='box'><p>[\1](../{week_id}/Flow/{flow_id})</p></div>", content)
  
  image_result: Result = await(
    db.execute(
      select(
        image_model.Image.id,
        image_model.Image.name
      ).where(image_model.Image.week_id == week_id)
    )
  )
  images = image_result.all()
  print(images)
  for image in images:
    image_id, image_name = image
    content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage](http://localhost:8000/get_image/{image_id})", content)
  image_name_to_id = {name: id for id, name in images}
  content = image_crud.replace_images_with_options(content, image_name_to_id)
    
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
  pages = page_result.all()
  print(pages)
  for page in pages:
    week_id, week_num, order, block_page = page
    content = re.sub(rf"\[(.*?)\]\s*\(\s*page/{week_num}/{order}/{block_page}\s*\)", rf"<div class='box'><p>[\1](../{week_id}/{block_page})</p></div>", content)
  

  await update_content(db=db, id=content_id, content=content)
  return {'success': True}

  

async def update_week_info(db: AsyncSession, user: user_schema.User, update_week_request: week_schema.UpdateWeekRequest):
  update_result: Result = await(
    db.execute(
      update(week_model.Week)
      .where(week_model.Week.id == update_week_request.week_id)
      .values(
        week_name = update_week_request.week_name,
        week_num = update_week_request.week_num,
        order = update_week_request.order
      )
    )
  )
  await db.commit()
  return {'success': True}










async def delete_week_content(db: AsyncSession, user: user_schema.User, delete_week_request: week_schema.DeleteWeekRequest):
  delete_result: Result = await(
    db.execute(
      update(week_model.Week)
      .where(week_model.Week.id == delete_week_request.week_id)
      .values(
        is_active = False
      )
    )
  )
  await db.commit()
  return {'success': True}








# 教科書コンテンツの更新
async def updateWeekContent(db: AsyncSession, week_id: int, content_id: int, origin_content_id: int, content: str):
  update_week_content_response = await update_week_content(db=db, week_id=week_id, content_id=content_id, origin_content_id=origin_content_id, content=content)
  return update_week_content_response

# week情報更新
async def update_week(db: AsyncSession, user: user_schema.User, update_week_request: week_schema.UpdateWeekRequest):
  update_week_response = await update_week_info(db=db, update_week_request=update_week_request, user=user)
  return update_week_response

# week削除（非表示）
async def delete_week(db: AsyncSession, user: user_schema.User, delete_week_request: week_schema.DeleteWeekRequest):
  delete_week_response = await delete_week_content(db=db, delete_week_request=delete_week_request, user=user)
  return delete_week_response

