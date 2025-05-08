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

import api.schemas.course as course_schema
import api.schemas.user as user_schema
import api.schemas.week as week_schema
import api.schemas.flow as flow_schema
import api.schemas.flow_page as flowpage_schema

import api.cruds.user as user_crud

async def update_flowpage(db: AsyncSession, user: user_schema.User, UpdateFlowPageRequest: flowpage_schema.UpdateFlowPageRequest):
    # flowpageのtitleを更新
    title_result: Result = await(db.execute(
        select(flowpage_model.FlowPage.title).where(flowpage_model.FlowPage.id == UpdateFlowPageRequest.flowpage_id)
    ))
    if UpdateFlowPageRequest.title != title_result.mappings().first()['title']:
        update_title_result: Result = await(
            db.execute(
                update(flowpage_model.FlowPage)
                .where(flowpage_model.FlowPage.id == UpdateFlowPageRequest.flowpage_id)
                .values(title = UpdateFlowPageRequest.title)
            )
        )
        await db.flush()
    
    # flowpageのcontentを更新
    content_result: Result = await(db.execute(
        select(content_model.Content.content).where(content_model.Content.id == UpdateFlowPageRequest.id_list.origin_content_id)
    ))
    if UpdateFlowPageRequest.content != content_result.mappings().first()['content']:
    
        update_content_result: Result = await(
            db.execute(
                update(content_model.Content)
                .where(content_model.Content.id == UpdateFlowPageRequest.id_list.origin_content_id)
                .values(content = UpdateFlowPageRequest.content)
            )
        )
    await db.commit()
    # flowpageのcontentを更新した結果を返す
    return True