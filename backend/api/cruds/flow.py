from fastapi import  Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert, update, func
from typing import List, Optional, Tuple
from jose import JWTError, jwt
from datetime import datetime
from zoneinfo import ZoneInfo
import re
import math
import random
import uuid
from collections import defaultdict

from api.db import get_db

import api.models.week as week_model
import api.models.course as course_model
import api.models.subject as subject_model
import api.models.user as user_model
import api.models.block as block_model
import api.models.content as content_model
import api.models.flow as flow_model
import api.models.flow_page as flow_page_model
import api.models.flow_session as flow_session_model
import api.models.page_group as page_group_model
import api.models.image as image_model

import api.schemas.week as week_schema
import api.schemas.course as course_schema
import api.schemas.user as user_schema
import api.schemas.flow as flow_schema
import api.schemas.flow_page as flow_page_schema
import api.schemas.content as content_schema

import api.cruds.user as user_crud
import api.cruds.update_week as update_week_crud
import api.cruds.image as image_crud
import api.cruds.create_week as create_week_crud

import os
from dotenv import load_dotenv
load_dotenv()

#Backend URL
BACKEND_URL = os.getenv('BACKEND_URL')

# フロー情報を取得
async def select_flow(db: AsyncSession, flow_id: int) -> flow_schema.FlowResponse:
  result: Result = await(
    db.execute(
      select(
        flow_model.Flow.title,
        flow_model.FlowRule.check_answer_timing,
        flow_model.FlowRule.challenge_limit,
        flow_model.FlowRule.restart_session,
        flow_model.FlowRule.time_limit,
        flow_model.FlowRule.start_date_time,
        flow_model.FlowRule.end_answer_date_time,
        flow_model.FlowRule.end_read_date_time,
        flow_model.FlowRule.always,
      ).where(flow_model.Flow.id == flow_id)
      .where(flow_model.Flow.id == flow_model.FlowRule.flow_id)
    )
  )
  return result.first()

# welcome_page_contentを取得
async def select_flow_welcome_page(db: AsyncSession, flow_id: int) -> flow_schema.ContentResponse:
  result: Result = await(
    db.execute(
      select(
        content_model.Content.content
      ).where(flow_model.Flow.id == flow_id)
      .where(flow_model.Flow.welcome_page_content_id == content_model.Content.id)
    )
  )
  return result.first()

async def select_flow_completion_page(db: AsyncSession, flow_id: int) -> flow_schema.ContentResponse:
  result: Result = await(
    db.execute(
      select(
        content_model.Content.content
      ).where(flow_model.Flow.id == flow_id)
      .where(flow_model.Flow.completion_page_content_id == content_model.Content.id)
    )
  )
  return result.first()

async def select_flow_sessions(db: AsyncSession, flow_id: int, user_id: int) -> List[flow_schema.FlowSessionResponse]:
  result: Result = await(
    db.execute(
      select(
        flow_session_model.FlowSession.id,
        flow_session_model.FlowSession.start_date_time,
        flow_session_model.FlowSession.finish_date_time,
        flow_session_model.FlowSession.is_finished,
        flow_session_model.FlowSession.flow_session_grade,
      ).where(flow_session_model.FlowSession.user_id == user_id)
      .where(flow_session_model.FlowSession.flow_id == flow_id)
    )
  )
  return result.all()

async def select_page_groups(db: AsyncSession, flow_id: int) -> List[flow_schema.ResponsePageGroup]:
  result: Result = await(
    db.execute(
      select(
        page_group_model.PageGroup.id,
        page_group_model.PageGroup.flow_id,
        page_group_model.PageGroup.order,
      ).where(page_group_model.PageGroup.flow_id == flow_id)
      .order_by(page_group_model.PageGroup.order)
    )
  )
  return result.mappings().all()

async def select_pagegroup_flowpages(db: AsyncSession, page_group_id: int):
  result: Result = await(
    db.execute(
      select(
        flow_page_model.FlowPage.page_group,
        flow_page_model.FlowPage.id,
        flow_page_model.FlowPage.order
      ).where(flow_page_model.FlowPage.page_group == page_group_id)
      .order_by(flow_page_model.FlowPage.order)
    )
  )
  return result.all()

async def select_single_text_question(db: AsyncSession, flowpage_id: int) -> flow_page_schema.SingleTextQuestionResponse:
  result: Result = await(
    db.execute(
      select(
        flow_page_model.SingleTextQuestion.id,
        content_model.Content.content,
        flow_page_model.Blank.id.label("blank_id")
      ).where(flow_page_model.SingleTextQuestion.id == flowpage_id)
      .where(flow_page_model.SingleTextQuestion.content_id == content_model.Content.id)
      .where(flow_page_model.SingleTextQuestion.id == flow_page_model.Blank.flowpage_id)
    )
  )
  return result.mappings().first()

async def select_multiple_text_question(db: AsyncSession, flowpage_id: int) -> flow_page_schema.MultipleTextQuestionResponse:
  content_result: Result = await(
    db.execute(
      select(
          flow_page_model.FlowPage.id,
          content_model.Content.content.label("content"),
      ).where(flow_page_model.FlowPage.id == flowpage_id)
      .where(flow_page_model.FlowPage.content_id == content_model.Content.id)
    )
  )
  answer_column_result: Result = await(
    db.execute(
      select(
        flow_page_model.MultipleTextQuestion.id,
        content_model.Content.content.label("answer_column_content"),
      ).where(flow_page_model.MultipleTextQuestion.id == flowpage_id)
      .where(flow_page_model.MultipleTextQuestion.answer_column_content_id == content_model.Content.id)
    )
  )
  content = content_result.mappings().first()["content"]
  answer_columns = answer_column_result.mappings().first()["answer_column_content"].split(',')
  print(answer_columns)
  answer_column = []
  for column in answer_columns:
    md, blank = column.split(':')
    print(md, blank)
    blank_id_result: Result = await(
      db.execute(
        select(
          flow_page_model.Blank.id
        ).where(flow_page_model.Blank.flowpage_id == flowpage_id)
        .where(flow_page_model.Blank.blank_name == blank)
      )
    )
    blank_id = blank_id_result.mappings().first()['id']
    print(blank_id)
    answer_column.append({'md': md, 'blank_name': blank, 'blank_id': blank_id})
  print(answer_column)
  return {"content": content, "answer_column_content": answer_column}

async def select_descriptive_text_question(db: AsyncSession, flowpage_id: int) -> flow_page_schema.DescriptiveTextQuestionResponse:
  result: Result = await(
    db.execute(
      select(
        content_model.Content.content,
        flow_page_model.Blank.id.label("blank_id")
      ).where(flow_page_model.DescriptiveTextQuestion.id == flowpage_id)
      .where(flow_page_model.DescriptiveTextQuestion.id == flow_page_model.FlowPage.id)
      .where(flow_page_model.DescriptiveTextQuestion.content_id == content_model.Content.id)
      .where(flow_page_model.DescriptiveTextQuestion.id == flow_page_model.Blank.flowpage_id)
    )
  )
  return result.mappings().first()

async def select_choice_question_choices(db: AsyncSession, flowpage_id: int) -> List[flow_page_schema.ChoiceQuestionChoiceResponse]:
  result: Result = await(
    db.execute(
      select(
        flow_page_model.ChoiceQuestionChoice.id,
        content_model.Content.content,
        flow_page_model.ChoiceQuestionChoice.order
      ).where(flow_page_model.ChoiceQuestionChoice.flowpage_id == flowpage_id)
      .where(flow_page_model.ChoiceQuestionChoice.content_id == content_model.Content.id)
    )
  )
  return result.mappings().all()

async def select_choice_question(db: AsyncSession, flowpage_id: int) -> flow_page_schema.ChoiceQuestionResponse:
  choice_question_result: Result = await(
    db.execute(
      select(
        content_model.Content.content,
        flow_page_model.Blank.id.label("blank_id")
      ).where(flow_page_model.ChoiceQuestion.id == flowpage_id)
      .where(flow_page_model.ChoiceQuestion.content_id == content_model.Content.id)
      .where(flow_page_model.ChoiceQuestion.id == flow_page_model.FlowPage.id)
      .where(flow_page_model.ChoiceQuestion.id == flow_page_model.Blank.flowpage_id)
    )
  )
  choice_result_dict = choice_question_result.mappings().first()
  choices_result = await select_choice_question_choices(db=db, flowpage_id=flowpage_id)
  response = {
    "content": choice_result_dict["content"],
    "blank_id": choice_result_dict["blank_id"],
    "choices": choices_result
  }
  return response

async def select_flowpage_answer_comments(db:AsyncSession, flowpage_id:int):
  result: Result = await(
    db.execute(
      select(
        content_model.Content.content
      ).where(flow_page_model.FlowPage.id == flowpage_id)
      .where(flow_page_model.FlowPage.answer_comment_id == content_model.Content.id)
    )
  )
  return result.mappings().first()

async def select_flow_session_flowpage(db: AsyncSession, flow_session_id: int, page: int):
  flow_page_result: Result = await(
    db.execute(
      select(
        flow_page_model.FlowPage.id,
        flow_page_model.FlowPage.title,
        flow_page_model.FlowPage.page_type
      ).where(flow_session_model.FlowSessionFlowPage.flow_session_id == flow_session_id)
      .where(flow_session_model.FlowSessionFlowPage.order == page)
      .where(flow_session_model.FlowSessionFlowPage.flowpage_id == flow_page_model.FlowPage.id)
    )
  )
  flow_page_dict = flow_page_result.mappings().first()
  page_type = flow_page_dict["page_type"]
  print(flow_page_dict)
  if page_type in ["single_text_question","SingleTextQuestion"]:
    page_type = "SingleTextQuestion"
    page_content = await select_single_text_question(db=db, flowpage_id = flow_page_dict["id"])
    answer_comment = await select_flowpage_answer_comments(db=db, flowpage_id = flow_page_dict["id"])
  elif page_type in ["multiple_text_question","MultipleTextQuestion"]:
    page_type = "MultipleTextQuestion"
    print(page_type)
    page_content = await select_multiple_text_question(db=db, flowpage_id = flow_page_dict["id"])
    print(page_content)
    answer_comment = await select_flowpage_answer_comments(db=db, flowpage_id = flow_page_dict["id"])
    print(answer_comment)
  elif page_type in ["descriptive_text_question","DescriptiveTextQuestion"]:
    page_type = "DescriptiveTextQuestion"
    page_content = await select_descriptive_text_question(db=db, flowpage_id = flow_page_dict["id"])
    answer_comment = await select_flowpage_answer_comments(db=db, flowpage_id = flow_page_dict["id"])
  elif page_type in ["choice_question","ChoiceQuestion"]:
    page_type = "ChoiceQuestion"
    page_content = await select_choice_question(db=db, flowpage_id = flow_page_dict["id"])
    answer_comment = await select_flowpage_answer_comments(db=db, flowpage_id = flow_page_dict["id"])
  else:
    raise ValueError(f"page_type: {page_type} is not defined.")

  response = {
    "title": flow_page_dict["title"],
    "page_type": page_type,
    "page_content": page_content,
    "answer_comment": answer_comment.content
  }
  print(f'response:{response}')
  return response

async def select_flow_session_flowpage_answer(db: AsyncSession, flow_session_id: int, page: int) -> List[flow_page_schema.BlankAnswerResponse]:
  latest_subquery = (
    select(
      flow_session_model.FlowSessionBlankAnswers.flowpage_id,
      flow_session_model.FlowSessionBlankAnswers.blank_id,
      func.max(flow_session_model.FlowSessionBlankAnswers.created).label('latest_created')
    ).group_by(flow_session_model.FlowSessionBlankAnswers.flowpage_id, flow_session_model.FlowSessionBlankAnswers.blank_id)
    .subquery()
  )
  result: Result = await(
    db.execute(
      select(
        flow_session_model.FlowSessionBlankAnswers.blank_id,
        flow_session_model.FlowSessionBlankAnswers.answer
      ).join(
        latest_subquery,
        (flow_session_model.FlowSessionBlankAnswers.flowpage_id == latest_subquery.c.flowpage_id) &
        (flow_session_model.FlowSessionBlankAnswers.blank_id == latest_subquery.c.blank_id) &
        (flow_session_model.FlowSessionBlankAnswers.created == latest_subquery.c.latest_created)
      ).where(flow_session_model.FlowSessionBlankAnswers.flow_session_id == flow_session_id)
      .where(flow_session_model.FlowSessionFlowPage.order == page)
      .where(flow_session_model.FlowSessionBlankAnswers.flow_session_id == flow_session_model.FlowSessionFlowPage.flow_session_id)
      .where(flow_session_model.FlowSessionBlankAnswers.flowpage_id == flow_session_model.FlowSessionFlowPage.flowpage_id)
    )
  )
  return result.all()

async def select_flow_info(db: AsyncSession, flow_session_id: int) -> flow_schema.FlowInfoResponse:
  result: Result = await(
    db.execute(
      select(
        flow_model.Flow.title.label('flow_title'),
        func.count('*').label('num_of_pages')
      ).where(flow_session_model.FlowSessionFlowPage.flow_session_id == flow_session_id)
      .where(flow_model.Flow.id == flow_session_model.FlowSession.flow_id)
      .where(flow_session_model.FlowSession.id == flow_session_model.FlowSessionFlowPage.flow_session_id)
    )
  )
  return result.mappings().first()
    
async def select_flowpage_hint_comments(db:AsyncSession, flow_session_id:int, page:int):
  result: Result = await(
    db.execute(
      select(
        content_model.Content.content
      ).where(flow_session_model.FlowSessionFlowPage.flow_session_id == flow_session_id)
      .where(flow_session_model.FlowSessionFlowPage.order == page)
      .where(flow_page_model.FlowPage.id == flow_session_model.FlowSessionFlowPage.flowpage_id)
      .where(flow_page_model.FlowPage.hint_comment_id == content_model.Content.id)
    )
  )
  return result.mappings().first()

async def select_flow_session_history(db: AsyncSession, user_id: int, course_id: int):
  result = []
  weeks_result: Result = await(
    db.execute(
      select(
        week_model.Week.id,
        week_model.Week.week_name
      ).where(course_id == week_model.Week.course_id)
      .order_by(week_model.Week.week_num, week_model.Week.order)
    )
  )
  weeks = weeks_result.mappings().all()
  for week in weeks:
    flows_result: Result = await(
      db.execute(
        select(
          flow_model.Flow.id,
          flow_model.Flow.title
        ).where(week.id == flow_model.Flow.week_id)
      )
    )
    flows = flows_result.mappings().all()
    flow_list = []
    for flow in flows:
      flow_sessions_result: Result = await(
        db.execute(
          select(
            flow_session_model.FlowSession.id,
            flow_session_model.FlowSession.finish_date_time,
            flow_session_model.FlowSession.flow_session_grade
          ).where(flow.id == flow_session_model.FlowSession.flow_id)
          .where(user_id == flow_session_model.FlowSession.user_id)
          .where(flow_session_model.FlowSession.is_finished == True)
        )
      )
      flow_sessions = flow_sessions_result.mappings().all()
      flow_session_list = []
      for flow_session in flow_sessions:
        flowpages_result: Result = await(
          db.execute(
            select(
              flow_page_model.FlowPage.id,
              content_model.Content.content
            ).where(flow_session.id == flow_session_model.FlowSessionFlowPage.flow_session_id)
            .where(flow_session_model.FlowSessionFlowPage.flowpage_id == flow_page_model.FlowPage.id)
            .where(flow_page_model.FlowPage.content_id == content_model.Content.id)
            .where(flow_session_model.FlowSessionFlowPage.is_correct == False)
            .where(flow_session_model.FlowSessionFlowPage.submitted == True)
            .order_by(flow_session_model.FlowSessionFlowPage.order)
          )
        )
        flow_session_list.append({
          'flow_session_id': flow_session.id,
          'finish_date_time': flow_session.finish_date_time,
          'flow_session_grade': flow_session.flow_session_grade,
          'flow_page': flowpages_result.mappings().all()
        })
      flow_list.append({flow.title: flow_session_list})
    result.append({week.week_name: flow_list})
  return result

async def select_week_flows(db: AsyncSession, week_id: int) -> List[flow_schema.WeekFlowsResponse]:
  result: Result = await(
    db.execute(
      select(
        flow_model.Flow.id,
        flow_model.Flow.title,
        flow_model.FlowRule.check_answer_timing,
        flow_model.FlowRule.challenge_limit,
        flow_model.FlowRule.restart_session,
        flow_model.FlowRule.time_limit,
        flow_model.FlowRule.start_date_time,
        flow_model.FlowRule.end_answer_date_time,
        flow_model.FlowRule.end_read_date_time,
        flow_model.FlowRule.always,
      ).where(flow_model.Flow.week_id == week_id)
      .where(flow_model.Flow.id == flow_model.FlowRule.flow_id)
      .where(flow_model.Flow.welcome_page_content_id == content_model.Content.id)
    )
  )
  return result.mappings().all()

async def select_student_score(db: AsyncSession, user_id: int, course_id: int):
  result = []
  weeks_result: Result = await(
    db.execute(
      select(
        week_model.Week.id,
        week_model.Week.week_name
      ).where(course_id == week_model.Week.course_id)
      .where(week_model.Week.is_active == True)
      .order_by(week_model.Week.week_num, week_model.Week.order)
    )
  )
  weeks = weeks_result.mappings().all()
  for week in weeks:
    flows_result: Result = await(
      db.execute(
        select(
          flow_model.Flow.id,
          flow_model.Flow.title
        ).where(week.id == flow_model.Flow.week_id)
      )
    )
    flows = flows_result.mappings().all()
    flow_list = []
    for flow in flows:
      flow_sessions_result: Result = await(
        db.execute(
          select(
            flow_session_model.FlowSession.id,
            flow_session_model.FlowSession.flow_session_grade,
            flow_session_model.FlowSession.finish_date_time
          ).where(flow.id == flow_session_model.FlowSession.flow_id)
          .where(user_id == flow_session_model.FlowSession.user_id)
          .where(flow_session_model.FlowSession.is_finished == True)
        )
      )
      flow_sessions = flow_sessions_result.mappings().all()
      flow_session_list = []
      for flow_session in flow_sessions:
        flow_session_list.append({
          'flow_session_id': flow_session.id if flow_session.id else 0,
          'flow_session_grade': flow_session.flow_session_grade if flow_session.flow_session_grade else 0,
          'finish_date_time' : flow_session.finish_date_time
        })
      if not flow_session_list:
        flow_session_list.append({
          'flow_session_id': 0,
          'flow_session_grade': 0,
        })
      flow_list.append({flow.title: flow_session_list})
    result.append({week.week_name: flow_list})
  return result

async def select_teacher_score(db: AsyncSession, course_id: int):
  result = []
  weeks_result: Result = await(
    db.execute(
      select(
        week_model.Week.id,
        week_model.Week.week_name
      ).where(course_id == week_model.Week.course_id)
      .where(week_model.Week.is_active == 1)
      .order_by(week_model.Week.week_num, week_model.Week.order)
    )
  )
  weeks = weeks_result.mappings().all()
  for week in weeks:
    flows_result: Result = await(
      db.execute(
        select(
          flow_model.Flow.id,
          flow_model.Flow.title
        ).where(week.id == flow_model.Flow.week_id)
      )
    )
    flows = flows_result.mappings().all()
    flow_list = []
    for flow in flows:
      flow_sessions_result: Result = await(
        db.execute(
          select(
            flow_session_model.FlowSession.id,
            flow_session_model.FlowSession.flow_session_grade
          ).where(flow.id == flow_session_model.FlowSession.flow_id)
          .where(flow_session_model.FlowSession.is_finished == True)
        )
      )
      flow_sessions = flow_sessions_result.mappings().all()
      flow_session_list = []
      for flow_session in flow_sessions:
        flow_session_list.append({
          'flow_session_id': flow_session.id if flow_session.id else 0,
          'flow_session_grade': flow_session.flow_session_grade if flow_session.flow_session_grade else 0,
        })
      flow_list.append({flow.title: flow_session_list})
    result.append({week.week_name: flow_list})
  return result

async def select_week_flowpage(db: AsyncSession, week_id: int):
  result = []
  flow_page_result: Result = await(
    db.execute(
      select(
        flow_page_model.FlowPage.id,
        flow_page_model.FlowPage.title,
        flow_page_model.FlowPage.page_type
      ).where(week_id == flow_model.Flow.week_id)
      .where(flow_model.Flow.id == page_group_model.PageGroup.flow_id)
      .where(page_group_model.PageGroup.id == flow_page_model.FlowPage.page_group)
    )
  )
  flow_pages = flow_page_result.mappings().all()
  
  for flowpage in flow_pages:
    content_id_result: Result = await(
      db.execute(
        select(
          flow_page_model.FlowPage.origin_content_id,
          flow_page_model.FlowPage.content_id,
          flow_page_model.FlowPage.origin_hint_comment_id,
          flow_page_model.FlowPage.hint_comment_id,
          flow_page_model.FlowPage.origin_answer_comment_id,
          flow_page_model.FlowPage.answer_comment_id,
        ).where(flowpage['id'] == flow_page_model.FlowPage.id)
      )
    )
    content_id_list = content_id_result.mappings().first()
    content_result: Result = await(db.execute(select(content_model.Content.content).where(content_id_list['origin_content_id'] == content_model.Content.id)))
    hint_comment_result: Result = await(db.execute(select(content_model.Content.content).where(content_id_list['origin_hint_comment_id'] == content_model.Content.id)))
    answer_comment_result: Result = await(db.execute(select(content_model.Content.content).where(content_id_list['origin_answer_comment_id'] == content_model.Content.id)))
    blank_result: Result = await(
      db.execute(
        select(
          flow_page_model.Blank.id,
          flow_page_model.Blank.blank_name,
          flow_page_model.CorrectAnswer.type,
          flow_page_model.CorrectAnswer.value
        ).where(flow_page_model.Blank.flowpage_id == flowpage['id'])
        .where(flow_page_model.Blank.id == flow_page_model.CorrectAnswer.blank_id)
      )
    )
    if flowpage['page_type'] in ['SingleTextQuestion', 'single_text_question', 'MultipleTextQuestion', 'multiple_text_question']:
      flowpage_content = {
        'flowpage_id': flowpage['id'],
        'title': flowpage['title'],
        'page_type': flowpage['page_type'],
        'id_list': {
          'origin_content_id': content_id_list['origin_content_id'],
          'content_id': content_id_list['content_id'],
          'origin_hint_comment_id': content_id_list['origin_hint_comment_id'],
          'hint_comment_id': content_id_list['hint_comment_id'],
          'origin_answer_comment_id': content_id_list['origin_answer_comment_id'],
          'answer_comment_id': content_id_list['answer_comment_id'],
        },
        'content': content_result.mappings().first()['content'],
        'hint_comment': hint_comment_result.mappings().first()['content'],
        'answer_comment': answer_comment_result.mappings().first()['content'],
        'blank_result': blank_result.mappings().all()
      }
    elif flowpage['page_type'] in ['ChoiceQuestion', 'choice_question']:
      choice_result: Result = await(
        db.execute(
          select(
            flow_page_model.ChoiceQuestionChoice.id,
            flow_page_model.ChoiceQuestionChoice.order,
            content_model.Content.content
          ).where(flowpage['id'] == flow_page_model.ChoiceQuestionChoice.flowpage_id)
          .where(content_model.Content.id == flow_page_model.ChoiceQuestionChoice.content_id)
        )
      )
      flowpage_content = {
        'flowpage_id': flowpage['id'],
        'title': flowpage['title'],
        'page_type': flowpage['page_type'],
        'id_list': {
          'origin_content_id': content_id_list['origin_content_id'],
          'content_id': content_id_list['content_id'],
          'origin_hint_comment_id': content_id_list['origin_hint_comment_id'],
          'hint_comment_id': content_id_list['hint_comment_id'],
          'origin_answer_comment_id': content_id_list['origin_answer_comment_id'],
          'answer_comment_id': content_id_list['answer_comment_id'],
        },
        'content': content_result.mappings().first()['content'],
        'hint_comment': hint_comment_result.mappings().first()['content'],
        'answer_comment': answer_comment_result.mappings().first()['content'],
        'blank_result': blank_result.mappings().all(),
        'choices': choice_result.mappings().all()
      }
    result.append(flowpage_content)
  return result

async def select_flowpages(db: AsyncSession, week_id: int):
  flow_result: Result = await(
    db.execute(
      select(
        flow_model.Flow.id,
        flow_model.Flow.id_in_yml,
        flow_model.Flow.title,
        flow_model.Flow.welcome_page_content_id,
        flow_model.Flow.completion_page_content_id,
      ).where(flow_model.Flow.week_id == week_id)
    )
  )
  flows = flow_result.mappings().all()
  
  result = []
  for flow in flows:
    welcome_page_content_result: Result = await(db.execute(select(content_model.Content.content).where(content_model.Content.id == flow['welcome_page_content_id'])))
    completion_page_content_result: Result = await(db.execute(select(content_model.Content.content).where(content_model.Content.id == flow['completion_page_content_id'])))
    page_group_result: Result = await(db.execute(select(
      page_group_model.PageGroup.id,
      page_group_model.PageGroup.group_name,
      page_group_model.PageGroup.order,
    ).where(page_group_model.PageGroup.flow_id == flow['id'])))
    page_groups = page_group_result.mappings().all()
    
    page_groups_result = []
    for page_group in page_groups:
      flowpage_result: Result = await(db.execute(select(
        flow_page_model.FlowPage.id,
        flow_page_model.FlowPage.title,
        flow_page_model.FlowPage.order,
        flow_page_model.FlowPage.page_type
      ).where(flow_page_model.FlowPage.page_group == page_group['id'])))
      flowpages = flowpage_result.mappings().all()
      
      flowpages_result = []
      for flowpage in flowpages:
        content_id_result: Result = await(db.execute(select(
          flow_page_model.FlowPage.origin_content_id,
          flow_page_model.FlowPage.content_id,
          flow_page_model.FlowPage.origin_hint_comment_id,
          flow_page_model.FlowPage.hint_comment_id,
          flow_page_model.FlowPage.origin_answer_comment_id,
          flow_page_model.FlowPage.answer_comment_id,
        ).where(flowpage['id'] == flow_page_model.FlowPage.id)))
        content_id_list = content_id_result.mappings().first()
        content_result: Result = await(db.execute(select(content_model.Content.content).where(content_id_list['origin_content_id'] == content_model.Content.id)))
        hint_comment_result: Result = await(db.execute(select(content_model.Content.content).where(content_id_list['origin_hint_comment_id'] == content_model.Content.id)))
        answer_comment_result: Result = await(db.execute(select(content_model.Content.content).where(content_id_list['origin_answer_comment_id'] == content_model.Content.id)))
        blank_result: Result = await(db.execute(select(
          flow_page_model.Blank.id,
          flow_page_model.Blank.blank_name,
          flow_page_model.CorrectAnswer.type,
          flow_page_model.CorrectAnswer.value
        ).where(flow_page_model.Blank.flowpage_id == flowpage['id'])
        .where(flow_page_model.Blank.id == flow_page_model.CorrectAnswer.blank_id)))
        blank = blank_result.mappings().all()
        # print(blank)
        if flowpage['page_type'] in ['MultipleTextQuestion', 'multiple_text_question']:
          multiple_result: Result = await(db.execute(select(
            content_model.Content.content
          ).where(flowpage['id'] == flow_page_model.MultipleTextQuestion.id)
          .where(flow_page_model.MultipleTextQuestion.answer_column_content_id == content_model.Content.id)))
          answer_columns = multiple_result.mappings().first()['content'].split(',')
          answer_column = {}
          updated_result = []
          for column in answer_columns:
            value, key = column.split(':')
            answer_column[key] = value
          for row in blank:
            row_dict = dict(row)
            row_dict['symble'] = answer_column[row_dict['blank_name']]
            row_dict['blank_id'] = row_dict['blank_name']
            updated_result.append(row_dict)
          blank = updated_result
        flowpage_content = {
          'flowpage_id': flowpage['id'],
          'title': flowpage['title'],
          'order': flowpage['order'],
          'page_type': flowpage['page_type'],
          'id_list': {
            'origin_content_id': content_id_list['origin_content_id'],
            'content_id': content_id_list['content_id'],
            'origin_hint_comment_id': content_id_list['origin_hint_comment_id'],
            'hint_comment_id': content_id_list['hint_comment_id'],
            'origin_answer_comment_id': content_id_list['origin_answer_comment_id'],
            'answer_comment_id': content_id_list['answer_comment_id'],
          },
          'content': content_result.mappings().first()['content'],
          'hint_comment': hint_comment_result.mappings().first()['content'],
          'answer_comment': answer_comment_result.mappings().first()['content'],
          'correct_answers': blank
        }          
        if flowpage['page_type'] in ['ChoiceQuestion', 'choice_question']:
          choice_result: Result = await(db.execute(select(
            flow_page_model.ChoiceQuestionChoice.id.label('choice_id'),
            flow_page_model.ChoiceQuestionChoice.order,
            content_model.Content.content.label('choice_text')
          ).where(flowpage['id'] == flow_page_model.ChoiceQuestionChoice.flowpage_id)
          .where(content_model.Content.id == flow_page_model.ChoiceQuestionChoice.content_id)))
          flowpage_content['choices'] =  choice_result.mappings().all()
        flowpages_result.append(flowpage_content)

      page_group_content = {
        'group_id': page_group['id'],
        'group_name': page_group['group_name'],
        'order': page_group['order'],
        'flowpages': flowpages_result
      }
      page_groups_result.append(page_group_content)
      
    welcome_page_content = welcome_page_content_result.mappings().first()['content']
    completion_page_content = completion_page_content_result.mappings().first()['content']
    flow_content = {
      'flow_id': flow['id'],
      'id_in_yml': flow['id_in_yml'],
      'flow_title': flow['title'],
      'id_list': {
        'welcome_page_content_id': flow['welcome_page_content_id'],
        'completion_page_content_id': flow['completion_page_content_id']
      },
      'welcome_page_content': welcome_page_content,
      'completion_page_content': completion_page_content,
      'page_groups' : page_groups_result
    }
    result.append(flow_content)
  return result 

async def flow_session_finished(db: AsyncSession, user_id: int,course_id : int):
  total = 0
  result = 0.0
  weeks_result: Result = await(
    db.execute(
      select(
        week_model.Week.id,
        week_model.Week.week_name
      ).where(course_id == week_model.Week.course_id)
      .order_by(week_model.Week.week_num, week_model.Week.order)
    )
  )
  weeks = weeks_result.mappings().all()
  for week in weeks:
    flows_result: Result = await(
      db.execute(
        select(
          flow_model.Flow.id,
          flow_model.Flow.title
        ).where(week.id == flow_model.Flow.week_id)
      )
    )
    flows = flows_result.mappings().all()
    total += len(flows)
    for flow in flows:
      flow_sessions_result: Result = await(
        db.execute(
          select(
            flow_session_model.FlowSession.flow_id,
            func.min(flow_session_model.FlowSession.flow_session_grade)
          ).where(flow.id == flow_session_model.FlowSession.flow_id)
          .where(user_id == flow_session_model.FlowSession.user_id)
          .where(flow_session_model.FlowSession.is_finished == True)
          .group_by(flow_session_model.FlowSession.flow_id)
        )
      )
      flow_sessions = flow_sessions_result.mappings().all()
      for flow_session in flow_sessions:
        flow_result: Result = await(
          db.execute(
            select(
              flow_model.Flow.id
            ).where(flow_session.flow_id == flow_model.Flow.id)
          )
        )
        result += len(flow_result.mappings().all())
  result = (result / total) * 100
  result = math.ceil(result)
  return result
'''
async def flow_session_finished(db: AsyncSession, user_id: int,subject_id : int):
  total = 0
  result = 0.0
  course_result : Result = await(
    db.execute(
      select(
        course_model.Course.id
      ).where(subject_id == course_model.Course.subject_id)
    )
  )
  courses = course_result.mappings().all()
  for course in courses:
    weeks_result: Result = await(
      db.execute(
        select(
          week_model.Week.id
        ).where(course.id == week_model.Week.course_id)
      )
    )
    weeks = weeks_result.mappings().all()
    for week in weeks:
      flows_result: Result = await(
        db.execute(
          select(
            flow_model.Flow.id,
            flow_model.Flow.title
          ).where(week.id == flow_model.Flow.week_id)
        )
      )
      flows = flows_result.mappings().all()
      total += len(flows)
      for flow in flows:
        flow_sessions_result: Result = await(
          db.execute(
            select(
              flow_session_model.FlowSession.id,
              flow_session_model.FlowSession.flow_id
            ).where(flow.id == flow_session_model.FlowSession.flow_id)
            .where(user_id == flow_session_model.FlowSession.user_id)
            .where(flow_session_model.FlowSession.is_finished == True)
          )
        )
        flow_sessions = flow_sessions_result.mappings().all()
        for flow_session in flow_sessions:
          flow_result: Result = await(
            db.execute(
              select(
                flow_model.Flow.id
              ).where(flow_session.flow_id == flow_model.Flow.id)
            )
          )
          result += len(flow_result.mappings().all())
  result = (result / total) * 100
  result = math.ceil(result)
  return result
'''
    





async def insert_flow_session(db: AsyncSession, flow_id: int, user_id: int) -> flow_schema.StartFlowSessionResponse:
  new_flow_session = flow_schema.FlowSessionCreate(user_id=user_id, flow_id=flow_id, start_date_time=datetime.now())
  row = flow_session_model.FlowSession(**new_flow_session.dict())
  db.add(row)
  await db.commit()
  await db.refresh(row)
  response = {"start_success": True, "flow_session_id": row.id, "start_date_time": row.start_date_time}
  return flow_schema.StartFlowSessionResponse(**response)

async def insert_flow_session_flow_page(db: AsyncSession, flow_session_flow_pages: List[flow_session_model.FlowSessionFlowPage]):
  db.add_all(flow_session_flow_pages)
  await db.commit()
  return

async def insert_blank_answer(db: AsyncSession, answer_blank_request: List[flow_page_schema.AnswerBlankRequest]) -> List[flow_schema.RegisterAnswerResponse]:
  response = []
  for answer_blank in answer_blank_request:
    result: Result = await(
      # flowsession_idとページ番号をもとに問題を特定して問題IDを受け取る処理
      db.execute(
        select(
          flow_session_model.FlowSessionFlowPage.flowpage_id,
        ).where(flow_session_model.FlowSessionFlowPage.flow_session_id == answer_blank.flow_session_id)
        .where(flow_session_model.FlowSessionFlowPage.order == answer_blank.page)
      )
    )
    flowpage_id = result.mappings().first()["flowpage_id"]
    print(f'flowpage_id:{flowpage_id}')
    new_flow_session_blank_answer = flow_schema.FlowSessionBlankAnswerCreate(
        flow_session_id=answer_blank.flow_session_id,
        flowpage_id=flowpage_id,
        blank_id=answer_blank.blank_id,
        answer=answer_blank.answer,
        created=datetime.now()
    )
    print(f'new_flow_session_blank_answer:{new_flow_session_blank_answer}')
    # 受け取った問題IDを元に解答を登録する処理
    row = flow_session_model.FlowSessionBlankAnswers(**new_flow_session_blank_answer.dict())
    db.add(row)
    # flowpage_idとblank_idを元に正答の一覧をSelectする処理をここに記述 これをユーザの解答と比較をして、True/False決定する.
    # 正答をもらってくる
    result: Result = await(
      db.execute(
        select(
          flow_page_model.CorrectAnswer.id,
          flow_page_model.Blank.flowpage_id,
          flow_page_model.CorrectAnswer.blank_id,
          flow_page_model.CorrectAnswer.type,
          flow_page_model.CorrectAnswer.value,
          flow_session_model.FlowSessionFlowPage.order,
        ).where(flow_session_model.FlowSession.id == flow_session_model.FlowSessionFlowPage.flow_session_id)
        .where(flow_session_model.FlowSessionFlowPage.flowpage_id == flow_page_model.FlowPage.id)
        .where(flow_page_model.FlowPage.id == flow_page_model.Blank.flowpage_id)
        .where(flow_page_model.Blank.id == flow_page_model.CorrectAnswer.blank_id)
        .where(flow_session_model.FlowSessionFlowPage.flowpage_id == flowpage_id)
        .where(flow_session_model.FlowSession.id == answer_blank.flow_session_id)
        .where(flow_page_model.CorrectAnswer.blank_id == answer_blank.blank_id)
      )
    )
    # 解答と正答の比較
    correct_answer_dict = result.mappings().all()
    print(f'correct_answer_dict:{correct_answer_dict}')
    # 問題の解答欄数をカウントする処理
    counter_result : Result = await(
      db.execute(
        select(
          flow_page_model.Blank.flowpage_id,
          flow_page_model.CorrectAnswer.blank_id
        ).where(flow_page_model.Blank.flowpage_id == flowpage_id)
        .where(flow_page_model.CorrectAnswer.blank_id == flow_page_model.Blank.id)
      )
    )
    counter_list = counter_result.mappings().all()
    counter_list = list(dict.fromkeys(counter_list))
    print(f'counter_list:{counter_list}')
    blank_answer_counter = len(counter_list)

    is_correct = False
    for correct_answer in correct_answer_dict:
      print(f'correct_answer:{correct_answer}')
      if str(answer_blank.answer) == str(correct_answer['value']):
        is_correct = True
      else:
        is_correct = False
    res_row = {'blank_id': correct_answer['blank_id'], 'is_correct': is_correct, 'correct_answer': correct_answer_dict[0]['value']}
    response += [res_row]
    is_submitted = False
    if len(response) != 0:
      is_submitted = True
    page_is_correct = False
    correct_cnt = 0
    for answers in response:
      if answers['is_correct'] == True:
        correct_cnt += 1

    # 正答数と、解答欄数が一致している条件を追加
    if len(response) == correct_cnt and correct_cnt == blank_answer_counter:
      page_is_correct = True
    else:
      page_is_correct = False
    # (update文で,flowsessionflowpageのis_correctに保存する ) ここまでの処理で入手した情報を RegisterAnswerResponseでwrapしてreturn する
    update_iscorrect: Result = await(
      db.execute(
        update(flow_session_model.FlowSessionFlowPage)
        .where(flow_session_model.FlowSessionFlowPage.flow_session_id == answer_blank.flow_session_id)
        .where(flow_session_model.FlowSessionFlowPage.flowpage_id == flowpage_id)
        .where(flow_session_model.FlowSessionFlowPage.order == answer_blank.page)
        .values(is_correct=page_is_correct)
        .values(submitted=is_submitted)
      )
    )
  await db.commit()
  return response

async def update_to_finish_flow_session(db: AsyncSession,user_id:int, flow_session_id: int) -> flow_schema.FlowSessionResponse:
  finish_date_time = datetime.now()
  result: Result = await(
    db.execute(
      update(flow_session_model.FlowSession)
      .where(flow_session_model.FlowSession.id == flow_session_id)
      .values(is_finished=True, finish_date_time=finish_date_time)
    )
  )
  point_result : Result = await(
    db.execute(
      update(user_model.User_com)
      .where(user_model.User_com.user_id == user_id)
      .values(point = user_model.User_com.point + 10)
    )
  )
  # flowsession_idとis_correctを参照して持ってくる
  grade_result: Result = await(
    db.execute(
      select(
          flow_session_model.FlowSessionFlowPage.flow_session_id,
          flow_session_model.FlowSessionFlowPage.submitted,
          flow_session_model.FlowSessionFlowPage.is_correct,
      ).where(flow_session_model.FlowSessionFlowPage.flow_session_id == flow_session_id)
    )
  )
  is_correct_dict = grade_result.mappings().all()
  answers = []
  for ans in is_correct_dict:
    if ans['submitted'] == True:
      answers.append(ans)

  # 正答率を求める処理
  cnt = 0
  grade = 0.0
  for i in range(len(answers)):
    if answers[i]['is_correct'] == True:
      cnt += 1
  if len(answers) != 0:
    grade = (cnt/len(answers))*100
  else:
    grade = 0.0
  response = {"finish_success": True, "finish_date_time": finish_date_time, "flow_session_grade": grade}
  # flow_session_gradeをdbのupdate文で保存
  update_grade: Result = await(
      db.execute(
          update(flow_session_model.FlowSession)
          .where(flow_session_model.FlowSession.id == flow_session_id)
          .values(flow_session_grade=grade)
      )
  )
  await db.commit()
  return response

async def update_question_content(db: AsyncSession, user: user_schema.User, update_question_request: flow_page_schema.UpdateQuestionRequest):
  content = update_question_request.content
  await update_week_crud.update_content(db=db, id=update_question_request.origin_content_id, content=content)
  image_result: Result = await(
    db.execute(
      select(
        image_model.Image.id,
        image_model.Image.name
      ).where(image_model.Image.week_id == update_question_request.week_id)
    )
  )
  images = image_result.all()
  for image in images:
    image_id, image_name = image
    content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage]({BACKEND_URL}/get_image/{image_id})", content)
  image_name_to_id = {name: id for id, name in images}
  content = image_crud.replace_images_with_options(content, image_name_to_id)
  await update_week_crud.update_content(db=db, id=update_question_request.content_id, content=content)
  return {'success': True}

async def update_choices_content(db: AsyncSession, user: user_schema.User, update_choices_request: flow_page_schema.UpdateChoicesRequest):
  for choice in update_choices_request.choice:
    update_result: Result = await(
      db.execute(
        update(content_model.Content)
        .where(flow_page_model.ChoiceQuestionChoice.flowpage_id == update_choices_request.flowpage_id)
        .where(flow_page_model.ChoiceQuestionChoice.id == choice.id)
        .where(content_model.Content.id == flow_page_model.ChoiceQuestionChoice.content_id)
        .values(
          content = choice.content
        )
      )
    )
  await db.commit()
  return {'success': True}

async def insert_content(db: AsyncSession, content: str):
  new_content = content_schema.ContentCreate(content=content)
  row = content_model.Content(**new_content.dict())
  db.add(row)
  await db.commit()
  await db.refresh(row)
  return row.id

async def update_content(db: AsyncSession, id: int, content: str):
  result: Result = await(
    db.execute(
      update(content_model.Content)
      .where(content_model.Content.id == id)
      .values(content=content)
    )
  )
  await db.flush()

async def update_flow_content(db: AsyncSession, flow: flow_schema.UpdateFlowRequest):
  await update_content(db=db, id=flow.welcome_page_content_id, content=flow.welcome_page_content)
  await update_content(db=db, id=flow.completion_page_content_id, content=flow.completion_page_content)
  update_flow = await(
    db.execute(
      update(flow_model.Flow)
      .where(flow_model.Flow.id == flow.flow_id)
      .values(
        title = flow.title,
        id_in_yml = flow.id_in_yml,
      )
    )
  )
  await db.commit()
  return

async def update_group_content(db: AsyncSession, group: flow_schema.UpdateGroupRequest):
  update_group = await(
    db.execute(
      update(page_group_model.PageGroup)
      .where(page_group_model.PageGroup.id == group.group_id)
      .values(
        group_name = group.group_name,
        order = group.order
      )
    )
  )
  await db.commit()
  return





async def is_readable_flow(db: AsyncSession, flow_id: int, user: user_schema.User):
  return True

async def is_startable_flow_session(db: AsyncSession, flow_id: int, user_id: int):
  return True

async def get_flow(db: AsyncSession, flow_id: int):
  return await select_flow(db=db, flow_id=flow_id)

async def get_flow_welcome_page(db: AsyncSession, flow_id: int):
  return await select_flow_welcome_page(db=db, flow_id=flow_id)

async def get_flow_completion_page(db: AsyncSession, flow_id: int):
  return await select_flow_completion_page(db=db, flow_id=flow_id)

async def get_flow_sessions(db: AsyncSession, flow_id: int, user_id: int):
  return await select_flow_sessions(db=db, flow_id=flow_id, user_id=user_id)

async def get_flow_session_flowpage(db: AsyncSession, flow_session_id: int, page: int):
  return await select_flow_session_flowpage(db=db, flow_session_id=flow_session_id, page=page)

async def get_flow_session_flowpage_answer(db: AsyncSession, flow_session_id: int, page: int):
  return await select_flow_session_flowpage_answer(db=db, flow_session_id=flow_session_id, page=page)

async def get_flow_info(db: AsyncSession, flow_session_id: int):
  return await select_flow_info(db=db, flow_session_id=flow_session_id)

async def get_flow_session_flowpage_hint(db: AsyncSession, flow_session_id: int, page: int):
  return await select_flowpage_hint_comments(db=db, flow_session_id=flow_session_id, page=page)

async def get_flow_session_flowpage_answer(db: AsyncSession, flow_session_id: int, page: int):
  return await select_flow_session_flowpage_answer(db=db, flow_session_id=flow_session_id, page=page)

async def get_flow_session_history(db: AsyncSession, user_id: int, course_id: int):
  return await select_flow_session_history(db=db, user_id=user_id, course_id=course_id)

async def get_week_flows(db: AsyncSession, week_id: int):
  return await select_week_flows(db=db, week_id=week_id)

async def get_flow_session_student_score(db: AsyncSession, user_id:int, course_id:int):
  return await select_student_score(db = db, user_id = user_id, course_id = course_id)

async def get_flow_session_teacher_score(db: AsyncSession, course_id:int):
  return await select_teacher_score(db = db,course_id = course_id)

async def get_week_flowpage(db: AsyncSession, week_id: int):
  #return await select_week_flowpage(db=db, week_id=week_id)
  return await select_flowpages(db=db, week_id=week_id)





async def start_new_flow_session(db: AsyncSession, flow_id: int, user_id: int):
  start_flow_session_response = await insert_flow_session(db=db, flow_id=flow_id, user_id=user_id)
  flow_groups = await select_page_groups(db=db, flow_id=flow_id)
  print(flow_groups)
  order_groups = defaultdict(list)
  for item in flow_groups:
    print(item)
    order_groups[item['order']].append(item)
  select_flow_group = []
  for order, group in order_groups.items():
    random.seed(datetime.now().microsecond)
    select_flow_group.append(random.choice(group))
  order_in_flow_session = 1
  flow_session_flow_page_list = []
  for flow_group in select_flow_group:
    pagegroup_flowpages = await select_pagegroup_flowpages(db=db, page_group_id=flow_group.id)
    for pagegroup_flowpage in pagegroup_flowpages:
      flow_session_flow_page_list += [
        flow_session_model.FlowSessionFlowPage(
          flow_session_id=start_flow_session_response.flow_session_id,
          flowpage_id=pagegroup_flowpage.id,
          order=order_in_flow_session,
          submitted=False
        )
      ]
      order_in_flow_session += 1
  await insert_flow_session_flow_page(db=db, flow_session_flow_pages=flow_session_flow_page_list)
  return start_flow_session_response

async def finish_flow_session(db: AsyncSession,user_id: int, flow_session_id: int):
  return await update_to_finish_flow_session(db=db,user_id = user_id, flow_session_id=flow_session_id)

async def register_blank_answer(db: AsyncSession, answer_blank_request: List[flow_page_schema.AnswerBlankRequest]):
    return await insert_blank_answer(db=db, answer_blank_request=answer_blank_request)

# 演習問題_問題文更新
async def update_question(db: AsyncSession, user: user_schema, update_question_request: flow_page_schema.UpdateQuestionRequest):
  update_question_response = await update_question_content(db=db, update_question_request=update_question_request, user=user)
  return update_question_response

# 演習問題_選択肢更新
async def update_choices(db: AsyncSession, user: user_schema, update_choices_request: flow_page_schema.UpdateChoicesRequest):
  update_choices_response = await update_choices_content(db=db, update_choices_request=update_choices_request, user=user)
  return update_choices_response

# 演習問題_flow登録
async def register_flow(db: AsyncSession, flow: flow_schema.RegisterFlowRequest):
  welcome_page_content_id = await insert_content(db=db, content=flow.welcome_page_content)
  completion_page_content_id = await insert_content(db=db, content=flow.completion_page_content)
  new_flow = flow_schema.FlowCreate(id_in_yml=flow.id_in_yml, week_id=flow.week_id, title=flow.title, welcome_page_content_id=welcome_page_content_id, completion_page_content_id=completion_page_content_id)
  row = flow_model.Flow(**new_flow.dict())
  print(f"row:{row}")
  db.add(row)
  await db.flush()
  await db.commit()
  return

# 演習問題_グループ登録
async def register_group(db: AsyncSession, group: flow_schema.RegisterGroupRequest):
  new_group = flow_schema.GroupCreate(flow_id=group.flow_id, group_name=group.group_name, order=group.order)
  row = page_group_model.PageGroup(**new_group.dict())
  db.add(row)
  await db.flush()
  await db.commit()
  return

# 演習問題_ページ登録
async def register_flowpage(db: AsyncSession, flowpage: flow_schema.RegisterFlowPageRequest):
  flow_content = flowpage.content
  hint_content = flowpage.hint_comment
  answer_content = flowpage.answer_comment
  images = await image_crud.get_images(db=db, week_id=flowpage.week_id)
  for image_id, image_name in [(img["id"], img["name"]) for img in images]:
    flow_content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage]({BACKEND_URL}/get_image/{image_id})", flow_content)
    flow_content = re.sub(f"\[\s*image/{image_name}\s*\]", f"<img src='{BACKEND_URL}/get_image/{image_id}' width='300' />", flow_content)
    hint_content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage]({BACKEND_URL}/get_image/{image_id})", hint_content)
    hint_content = re.sub(f"\[\s*image/{image_name}\s*\]", f"<img src='{BACKEND_URL}/get_image/{image_id}' width='300' />", hint_content)
    answer_content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage]({BACKEND_URL}/get_image/{image_id})", answer_content)
    answer_content = re.sub(f"\[\s*image/{image_name}\s*\]", f"<img src='{BACKEND_URL}/get_image/{image_id}' width='300' />", answer_content)
  origin_content_id = await insert_content(db=db, content=flowpage.content)
  content_id = await insert_content(db=db, content=flow_content)
  origin_hint_comment_id = await insert_content(db=db, content=flowpage.hint_comment)
  hint_comment_id = await insert_content(db=db, content=hint_content)
  origin_answer_comment_id = await insert_content(db=db, content=flowpage.answer_comment)
  answer_comment_id = await insert_content(db=db, content=answer_content)
  page_type = flowpage.page_type
  if page_type in ["single_text_question", "SingleTextQuestion"]:
    await create_week_crud.add_single_text_question(db=db, flowpage=flowpage.dict(), content_id=content_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, hint_comment_id=hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, answer_comment_id=answer_comment_id, page_group_id=flowpage.group_id)
  if page_type in ["multiple_text_question", "MultipleTextQuestion"]:
    symble_dict = defaultdict(set)
    for item in flowpage.correct_answers:
      symble = item['symble']
      blank_id = item["blank_id"]
      symble_dict[symble].add(blank_id)
    answer_column = " ".join(f"{symble}:[[{' '.join(sorted(blanks))}]]" for symble, blanks in sorted(symble_dict.items()))
    flowpage=flowpage.dict()
    flowpage["answer_column"] = answer_column
    grouped = defaultdict(list)
    for ans in flowpage["correct_answers"]:
      grouped[ans["blank_id"]].append({
        "type": ans["type"],
        "value": int(ans["value"]) if ans["type"] == "int" else ans["value"]
      })
    flowpage["correct_answers"] = [{"blank_id": k, "answers": v} for k, v in grouped.items()]
    print(f"******flowpage['correct_answers']:{flowpage['correct_answers']}")
    await create_week_crud.add_multiple_text_question(db=db, content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, flowpage=flowpage, page_group_id=flowpage["group_id"])
  if page_type in ["descriptive_text_question", "DescriptiveTextQuestion"]:
    await create_week_crud.add_descriptive_text_question(db=db, content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, flowpage=flowpage.dict(), page_group_id=flowpage.group_id)
  if page_type in ["choice_question", "ChoiceQuestion"]:
    sorted_choices = [{k: v for k, v in choice.items() if k != 'id'} for choice in sorted(flowpage.choices, key=lambda x: x['order'])]
    flowpage.choices = sorted_choices
    await create_week_crud.add_choice_question(db=db, content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, flowpage=flowpage.dict(), page_group_id=flowpage.group_id)
  await db.commit()
  return


# 演習問題_flow更新
async def update_flow(db: AsyncSession, flow: flow_schema.UpdateFlowRequest):
  update_flow_response = await update_flow_content(db=db, flow=flow)
  return update_flow_response

# 演習問題_グループ更新
async def update_group(db: AsyncSession, group: flow_schema.UpdateGroupRequest):
  update_group_response = await update_group_content(db=db, group=group)
  return update_group_response


