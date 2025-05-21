
from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, insert, update
from typing import List, Optional, Tuple
import datetime
from zoneinfo import ZoneInfo

import api.models.course as course_model
import api.models.week as week_model
import api.models.content as content_model
import api.models.block as block_model
import api.models.flow as flow_model
import api.models.page_group as page_group_model
import api.models.flow_page as flow_page_model
import api.models.image as image_model
# import api.models.math_keywords as math_keywords_model

import api.schemas.user as user_schema
import api.schemas.content as content_schema
import api.schemas.block as block_schema
import api.schemas.course as course_schema
import api.schemas.week as week_schema
import api.schemas.flow as flow_schema
import api.schemas.page_group as page_group_schema
import api.schemas.flow_page as flow_page_schema
import api.schemas.image as image_schema

import api.cruds.image as image_crud

import yamale
import yaml
import traceback
import re
import uuid

import os
from dotenv import load_dotenv
load_dotenv()

#Backend URL
BACKEND_URL = os.getenv('BACKEND_URL')
class YamlFormatter():
  # 初期設定
  def __init__(self, files: List[week_schema.RegisterWeekRequest], flow_list, page_list):
    self.directory_structure = self.create_directory_structure(files)
    self.block_yml_list = []
    self.flow_yml_list = []
    self.image_dict = {}
    self.flow = []
    self.image = []
    self.flow_list = flow_list
    self.page_list = page_list

  # アップロードされたファイルに入っているファイルの構造を辞書型に変換    
  def create_directory_structure(self, files: List[week_schema.RegisterWeekRequest]):
    directory_structure = {}
    for file in files:
      new_dict = directory_structure
      splited_path = file.file_path.split('/')
      file_name = splited_path[-1]
      for dir in splited_path[:-1]:
        if dir in new_dict:
          new_dict = new_dict[dir]
        else:
          new_dict[dir] = {}
          new_dict = new_dict[dir]
      new_dict[file_name] = file.file_text
    return directory_structure
  
  def validate_files(self):
    error_msg = ''
    
    # アップロードされたファイルのバリデーション
    if len(self.directory_structure.keys()) != 1:
      error_msg += 'ルートディレクトリは1つにしてください'
      return {'success': False, 'error_msg': error_msg}
    # ルートディレクトリの設定
    self.root_directory = list(self.directory_structure.keys())[0]
    ## print(root_directory)

    # blockのバリデーション
    block_validation_success = True
    # blocksのディレクトリが存在するか
    if 'blocks' in self.directory_structure[self.root_directory]:
      # blocks内に含まれるファイル名を取得
      block_files = self.directory_structure[self.root_directory]['blocks'].keys()
      # blocks内に1つ以上ファイルが含まれているか
      if len(block_files) > 0:
        for block_file in block_files:
          # blocksに含まれるファイルの中にymlファイル以外が入っていないかチェック
          if not re.match('.*\.(yaml|yml)$', block_file):
            error_msg += f'{block_file} is not yml_file\n'
          block_validate = self.validate_block(self.directory_structure[self.root_directory]['blocks'][block_file])
          ### print(block_validate)
          block_validation_success = block_validation_success and block_validate['success']
          if not block_validation_success:
            error_msg += '\n'.join(block_validate['error_msgs'])
      else:
        error_msg += '\nblock files is not found.'
        return {'success': False, 'error_msg': error_msg}
    else:
      error_msg += '\nblocks directory is not found'
      return {'success': False, 'error_msg': error_msg}
    
    # flowのバリデーション
    flow_validation_success = True
    if len(self.flow) > 0:
      flow_files = self.directory_structure[self.root_directory]['flows'].keys()
      for flow_file in flow_files:
        if not re.match('.*\.(yaml|yml)$', flow_file):
          error_msg += f"{flow_file} is not yml_file\n"
        flow_validate = self.validate_flow(self.directory_structure[self.root_directory]['flows'][flow_file])
        ### print(flow_validate)
        flow_validation_success = flow_validation_success and flow_validate['success']
        if not flow_validation_success:
          error_msg += '\n'.join(flow_validate['error_msgs'])
                
    # image_dict {ファイル名：バイナリデータ}の追加
    if len(self.image) > 0:
      image_files = self.directory_structure[self.root_directory]['images'].keys()
      for image_name in image_files:
        if not re.match('.*\.(jpeg|jpg|png|svg)$', image_name):
          error_msg += f"{image_name} is not yml_file\n"
        image_data = self.directory_structure[self.root_directory]['images'][image_name]
        self.image_dict[image_name] = image_data.encode()
    
    ## print(f'block_yml_list\n{self.block_yml_list}')
    ## print(f'flow_yml_list\n{self.flow_yml_list}')
    ## print(f'image_dict\n{self.image_dict}')
    ## print(f'flow\n{self.flow}')
    ## print(f'image\n{self.image}')
    return {'success': block_validation_success and flow_validation_success, 'error_msg': error_msg}
    
  def validate_block(self, yml_text: str):
    validate_error = []
    try:
      # blocksに含まれるファイルの形式が正しいか
      schema = yamale.make_schema('./api/yaml_validation_schemas/block.yml')
      block_yml_dict = yaml.safe_load(yml_text)
      self.block_yml_list += [block_yml_dict]
      block_data = [(block_yml_dict, '')]
      yamale.validate(schema, block_data)
      
      # flowリンクの存在チェック
      ## print(yml_text)
      flow_links = re.findall('\(\s*flow/\s*\s*(.+?)\s*\)', yml_text, re.S)
      ## print(flow_links)
      print(self.flow_list)
      if 'flows' in self.directory_structure[self.root_directory] and len(flow_links) > 0:
        for link in flow_links:
          if not link + '.yml' in self.directory_structure[self.root_directory]['flows']:
            flow_result = [flow for flow in self.flow_list if flow['id_in_yml'] == link]
            if not flow_result:
              validate_error += [f"flow_file '{link}' is not found."]
          elif link not in self.flow:
            self.flow += [link]
      elif len(flow_links) > 0:
        validate_error += [f"flows directory is not found."]
      
      # imageリンクの存在チェック
      image_links = re.findall('\(\s*image\s*/\s*(.+?)\s*\)', yml_text, re.S)
      image_links += re.findall('\[\s*image\s*/\s*(.+?)\s*\]', yml_text, re.S)
      ## print(image_links)
      if 'images' in self.directory_structure[self.root_directory] and len(image_links) > 0:
        for link in image_links:
          if not link in self.directory_structure[self.root_directory]['images']:
            validate_error += [f"image_file '{link}' is not found."]
          elif link not in self.image:
            self.image += [link]
      elif len(image_links) > 0:
        validate_error += [f"images directory is not found."]
        
    except ValueError as e:
      t = traceback.format_exception_only(type(e), e)
      validate_error += t
    return {'success': len(validate_error) == 0, 'error_msgs': validate_error}

  def replace_scripts(self, yml_text: str):
    scripts = re.findall('(\s*?){{\s*(.+?)\s*\((.+?)\)\s*}}', yml_text)
    for script in scripts:
      num_indent_spaces = len(script[0])
      if script[1] == 'include':
        included_yml = self.get_file_by_path(script[2])
        included_yml = self.replace_scripts(included_yml)
        included_yml_with_indent = '\n'
        for line in included_yml.split('\n'):
          new_line = ' ' * num_indent_spaces + line + '\n'
          included_yml_with_indent += new_line
        yml_text = re.sub(f'{script[0]}{{{{\s*{script[1]}\s*\({script[2]}\)\s*}}}}', included_yml_with_indent.replace("\\", "\\\\"), yml_text)
    return yml_text

  def get_file_by_path(self, path):
    path_splited = path.split('/')
    file_name = path_splited[-1]
    d = self.directory_structure[self.root_directory]
    for dir in path_splited[:-1]:
      d = d[dir]
    return d[file_name]

  def validate_flow(self, yml_text: str):
    validate_error = []
    try:
      yml_text = self.replace_scripts(yml_text=yml_text)
      schema = yamale.make_schema('./api/yaml_validation_schemas/flow.yml')
      flow_yml_dict = yaml.safe_load(yml_text)
      self.flow_yml_list += [flow_yml_dict]
      flow_data = [(flow_yml_dict, '')]
      yamale.validate(schema, flow_data)
      
      # imageリンクの存在チェック
      image_links = re.findall('\(\s*image\s*/\s*(.+?)\s*\)', yml_text, re.S)
      ## print(image_links)
      if 'images' in self.directory_structure[self.root_directory] and len(image_links) > 0:
        for link in image_links:
          if not link in self.directory_structure[self.root_directory]['images']:
            validate_error += [f"image_file '{link}' is not found."]
          elif link not in self.image:
            self.image += [link]
      elif len(image_links) > 0:
        validate_error += [f"images directory is not found."]
      
      # ページタイプ別バリデーション
      for page_group in flow_yml_dict['page_groups']:
        for page in page_group['pages']:
          page_data = [(page, '')]
          try:
            # SingleTextQuestionのバリデーション
            if page['page_type'] in ['SingleTextQuestion', 'single_text_question']:
              schema = yamale.make_schema('./api/yaml_validation_schemas/pages/single_text_question.yml')
              yamale.validate(schema, page_data)
            # MultipleTextQuestionのバリデーション
            elif page['page_type'] in ["MultipleTextQuestion", "multiple_text_question"]:
              schema = yamale.make_schema('./api/yaml_validation_schemas/pages/multiple_text_question.yml')
              yamale.validate(schema, page_data)
              # blank_idのチェック
              answer_column_blank_id = re.findall('\[\[(.+?)\]\]', page["answer_column"])
              correct_answer_blank_id = [v["blank_id"] for v in page["correct_answers"]]
              if len(answer_column_blank_id) != len(set(answer_column_blank_id)):
                raise ValueError('There is blank_id duplicate in answer_column.')
              if len(correct_answer_blank_id) != len(set(answer_column_blank_id)):
                raise ValueError('There is blank_id duplicate in correct_answers.')
              if not set(answer_column_blank_id) == set(correct_answer_blank_id):
                raise ValueError("There is no ID correspondence between answer_column and correct_answers.")
            # DescriptiveTextQuestionのバリデーション
            elif page['page_type'] in ["DescriptiveTextQuestion", "descriptive_text_question"]:
              schema = yamale.make_schema('./api/yaml_validation_schemas/pages/descriptive_text_question.yml')
              yamale.validate(schema, page_data)
            # ChoiceQuestionのバリデーション
            elif page['page_type'] in ["ChoiceQuestion", "choice_question"]:
              schema = yamale.make_schema('./api/yaml_validation_schemas/pages/choice_question.yml')
              yamale.validate(schema, page_data)
              # choice_idのチェック
              choice_id = [v['choice_id'] for v in page['choices']]
              correct_choice_id = page['correct_choices']
              if len(choice_id) != len(set(choice_id)):
                raise ValueError("There is blank_id duplicate in choices.")
              if len(correct_choice_id) != len(set(correct_choice_id)):
                raise ValueError("There is blank_id duplicate in correct_choices.")
              if not set(choice_id) >= set(correct_choice_id):
                raise ValueError("There is no ID correspondence between choices and correct_choices.")
            # 該当するページタイプがない場合
            else:
              raise ValueError(f"page_type: {page['page_type']} is not defined.")
          except ValueError as e:
            t = traceback.format_exception_only(type(e), e)
            validate_error += t
    except ValueError as e:
      t = traceback.format_exception_only(type(e), e)
      validate_error += t
    return {'success': len(validate_error)==0, 'error_msgs': validate_error}

async def add_week_file(db: AsyncSession, user_with_grant: user_schema.UserWithGrant, register_week_request: week_schema.RegisterWeekRequest, block_yml_list: List[dict], flow_yml_list: List[dict], image_dict: dict, flow_list, page_list) -> week_schema.RegisterWeekResponse:
  # コースの追加
  registered_week = await add_week(db=db, user_with_grant=user_with_grant, register_week_request=register_week_request)
  
  # 画像の追加
  id_in_image_name = {}
  for image_name, image_data in image_dict.items():
    image_id = await add_image(db=db, image_name=image_name, week_id=registered_week.id, image_data=image_data)
    id_in_image_name[image_id] = image_name
  
  # Flowの追加
  id_in_yml_flow_id_dict = {}
  for flow in flow_yml_list:
    flow_id = await add_flow(db, registered_week.id, flow)
    id_in_yml_flow_id_dict[flow['id']] = flow_id
    await add_flow_grant(db, flow_id, user_with_grant.id)
    if 'rules' in flow:
      await add_flow_rule(db, flow_id, flow['rules'])
    else:
      await add_flow_rule(db, flow_id)
    for page_group in flow['page_groups']:
      page_group_id = await add_page_group(db, flow_id, page_group)
      
      # FlowPageの追加
      for page in page_group['pages']:
        flowpage_id = await add_flowpage(db=db, flowpage=page, id_in_image_name=id_in_image_name, page_group_id=page_group_id)
  
  # Blockの追加
  for block in block_yml_list:
    content = block['content']
    # 既存のflowへのリンク設定
    for flow in flow_list:
      print(f"flow:{flow}")
      flow_id = flow['flow_id']
      id_in_yml = flow['id_in_yml']
      week_id = flow['week_id']
      content = re.sub(rf"\[(.*?)\]\s*\(\s*flow/{id_in_yml}\s*\)", rf"<div class='box'><p>[\1](../{week_id}/Flow/{flow_id})</p></div>", content)
    # flowへのリンク設定 (flow/{id_in_yml}) -> (flow/{flow_id})
    for id_in_yml, flow_id in id_in_yml_flow_id_dict.items():
      #content = re.sub(f"\(\s*flow/{id_in_yml}\s*\)", f"<div class='box'><p>(Flow/{flow_id})</p></div>", content)
      content = re.sub(rf"\[(.*?)\]\s*\(\s*flow/{id_in_yml}\s*\)", rf"<div class='box'><p>[\1](Flow/{flow_id})</p></div>", content)
    # imageの取得設定 (image/{image_name}) -> ![contentsimage](http://~/get_image/{image_id})
    for image_id, image_name in id_in_image_name.items():
      content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage]({BACKEND_URL}/get_image/{image_id})", content)
    image_name_to_id = {v: k for k, v in id_in_image_name.items()}
    content = image_crud.replace_images_with_options(content, image_name_to_id)
    # pageへのリンク設定 (page/{week_num}/{order}/{block_page}) -> (../{week_id}/{block_page})
    for page in page_list:
      week_id = page['week_id']
      week_num = page['week_num']
      order = page['order']
      block_page = page['page']
      content = re.sub(rf"\[(.*?)\]\s*\(\s*page/{week_num}/{order}/{block_page}\s*\)", rf"<div class='box'><p>[\1](../{week_id}/{block_page})</p></div>", content)
    # db登録
    content_id = await add_content(db=db, content=content)
    origin_content_id = await add_content(db=db, content=block['content'])
    block_id = await add_block(db=db, week_id=registered_week.id, page=block['page'], content_id=content_id, origin_content_id=origin_content_id)
    # rule登録
    if 'rules' in block:
      await add_block_rules(db=db, block_id=block_id, rules=block['rules'])
    else:
      await add_block_rules(db=db, block_id=block_id)
    # コースキーワード登録
    
  await db.commit()
  return {'success': True, 'error_msg': '', 'registered_week': registered_week}
    
  

async def add_content(db: AsyncSession, content: str):
  new_content = content_schema.ContentCreate(content=content)
  row = content_model.Content(**new_content.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return row.id

async def add_image(db: AsyncSession, image_name: str, week_id: int, image_data: bytes):
  new_image = image_schema.ImageCreate(name=image_name, week_id=week_id, imgdata=image_data)
  row = image_model.Image(**new_image.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return row.id

async def add_week(db: AsyncSession, user_with_grant: user_schema.UserWithGrant, register_week_request: week_schema.RegisterWeekRequest):
  new_week = week_schema.WeekCreate(course_id=register_week_request.course_id, week_name=register_week_request.week_name, week_num=register_week_request.week_num, order=register_week_request.order, created_by=user_with_grant.id)
  row = week_model.Week(**new_week.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return week_schema.RegisteredWeek(id=row.id, course_id=register_week_request.course_id, week_name=register_week_request.week_name, week_num=register_week_request.week_num, order=register_week_request.order, created=row.created)

async def add_flow(db: AsyncSession, week_id: int, flow_dict: dict):
  # コンテンツの登録
  welcome_page_content_id = await add_content(db=db, content=flow_dict['welcome_page_content'])
  completion_page_content_id = await add_content(db=db, content=flow_dict['completion_page_content'])
  new_flow = flow_schema.FlowCreate(id_in_yml=flow_dict['id'], week_id=week_id, title=flow_dict['title'], welcome_page_content_id=welcome_page_content_id, completion_page_content_id=completion_page_content_id)
  row = flow_model.Flow(**new_flow.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return row.id

async def add_flow_grant(db: AsyncSession, flow_id: int, user_id: int):
  new_flow_grant = flow_schema.FlowGrantCreate(user_id=user_id, flow_id=flow_id, start_date_time=datetime.datetime.now(), end_date_time=datetime.datetime.now()+datetime.timedelta(days=365), read_answer=True, update_answer=True, delete_answer=True)
  row = flow_model.FlowGrant(**new_flow_grant.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return

async def add_flow_rule(db: AsyncSession, flow_id: int, rules=None):
  new_flow_rule = flow_schema.FlowRuleCreate(flow_id=flow_id)
  if rules != None:
    if "check_answer_timing" in rules:
        new_flow_rule.check_answer_timing = rules["check_answer_timing"]
    if "challenge_limit" in rules:
        new_flow_rule.challenge_limit = rules["challenge_limit"]
    if "restart_session" in rules:
        new_flow_rule.restart_session = rules["restart_session"]
    if "time_limit" in rules:
        new_flow_rule.time_limit = rules["time_limit"]
    if "start_date_time" in rules:
        new_flow_rule.start_date_time = rules["start_date_time"]
    if "end_answer_date_time" in rules:
        new_flow_rule.end_answer_date_time = rules["end_answer_date_time"]
    if "end_read_date_time" in rules:
        new_flow_rule.end_read_date_time = rules["end_read_date_time"]
    if "always" in rules:
        new_flow_rule.always = rules["always"]
  row = flow_model.FlowRule(**new_flow_rule.dict())
  db.add(row)
  db.flush()
  db.refresh(row)
  return

async def add_page_group(db: AsyncSession, flow_id: int, page_group: dict):
  new_page_groups = page_group_schema.PageGroupCreate(group_name=page_group['group_name'], flow_id=flow_id, order=page_group['order'])
  row = page_group_model.PageGroup(**new_page_groups.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return row.id
  
async def add_flowpage(db: AsyncSession, flowpage: dict, id_in_image_name: dict, page_group_id: int):
  flow_content = flowpage['content']
  hint_content = flowpage['hint_comment']
  answer_content = flowpage['answer_comment']
  for image_id, image_name in id_in_image_name.items():
    flow_content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage]({BACKEND_URL}/get_image/{image_id})", flow_content)
    hint_content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage]({BACKEND_URL}/get_image/{image_id})", hint_content)
    answer_content = re.sub(f"\(\s*image/{image_name}\s*\)", f"![contentsimage]({BACKEND_URL}/get_image/{image_id})", answer_content)
  image_name_to_id = {v: k for k, v in id_in_image_name.items()}
  flow_content = image_crud.replace_images_with_options(flow_content, image_name_to_id)
  hint_content = image_crud.replace_images_with_options(hint_content, image_name_to_id)
  answer_content = image_crud.replace_images_with_options(answer_content, image_name_to_id)
  content_id = await add_content(db, flow_content)
  hint_comment_id = await add_content(db, hint_content)
  answer_comment_id = await add_content(db, answer_content)
  origin_content_id = await add_content(db, flowpage['content'])
  origin_hint_comment_id = await add_content(db, flowpage['hint_comment'])
  origin_answer_comment_id = await add_content(db, flowpage['answer_comment'])
  page_type = flowpage['page_type']
  if page_type in ["single_text_question", "SingleTextQuestion"]:
    return await add_single_text_question(db=db, content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, flowpage=flowpage, page_group_id=page_group_id)
  if page_type in ["multiple_text_question", "MultipleTextQuestion"]:
    return await add_multiple_text_question(db=db, content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, flowpage=flowpage, page_group_id=page_group_id)
  if page_type in ["descriptive_text_question", "DescriptiveTextQuestion"]:
    return await add_descriptive_text_question(db=db, content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, flowpage=flowpage, page_group_id=page_group_id)
  if page_type in ["choice_question", "ChoiceQuestion"]:
    return await add_choice_question(db=db, content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, flowpage=flowpage, page_group_id=page_group_id)
  else:
    raise ValueError(f"page_type {page_type} is not defined.")

async def add_blank(db: AsyncSession, flowpage_id: int, blank_name: str):
  new_blank = flow_page_schema.BlankCreate(blank_name=blank_name, flowpage_id=flowpage_id)
  row = flow_page_model.Blank(**new_blank.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return row.id

async def add_correct_answer(db: AsyncSession, blank_id: int, correct_answer: dict):
  new_correct_answer = flow_page_schema.CorrectAnswerCreate(blank_id=blank_id, type=correct_answer['type'], value=str(correct_answer['value']))
  print(f"**add*{new_correct_answer}")
  row = flow_page_model.CorrectAnswer(**new_correct_answer.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return

async def add_single_text_question(db: AsyncSession, content_id: int, hint_comment_id: int, answer_comment_id: int, origin_content_id: int, origin_hint_comment_id: int, origin_answer_comment_id: int, flowpage: dict, page_group_id: int):
  new_single_text_question = flow_page_schema.SingleTextQuestionCreate(content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, title=flowpage['title'], page_type=flowpage['page_type'], page_group=page_group_id, order=flowpage['order'])
  row = flow_page_model.SingleTextQuestion(**new_single_text_question.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  flowpage_id = row.id
  
  # 解答欄と正答情報を追加
  blank_name = 'blank_' + str(uuid.uuid4())
  blank_id = await add_blank(db=db, blank_name=blank_name, flowpage_id=flowpage_id)
  if not 'correct_answer' in flowpage:
    flowpage['correct_answer'] = flowpage['correct_answers']
  for correct_answer in flowpage['correct_answer']:
    await add_correct_answer(db=db, blank_id=blank_id, correct_answer=correct_answer)
  return flowpage_id

async def add_multiple_text_question(db: AsyncSession, content_id: int, hint_comment_id: int, answer_comment_id: int, origin_content_id: int, origin_hint_comment_id: int, origin_answer_comment_id: int, flowpage: dict, page_group_id: int):
  pattern = r'(\S+):\s*\[\[([^\]]+)\]\]'
  answer_column = flowpage['answer_column']
  print(f'answer_column_01:{answer_column}')
  answer_column = re.findall(pattern, answer_column)
  print(f'answer_column_02:{answer_column}')
  answer_content = ','.join([f"{key}:{value}" for key, value in answer_column])
  print(f'answer_content:{answer_content}')
  answer_column_content_id = await add_content(db=db, content=answer_content)
  origin_answer_column_content_id = await add_content(db=db, content=flowpage['answer_column'])
  new_multiple_text_question = flow_page_schema.MultipleTextQuestionCreate(content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, title=flowpage['title'], page_type=flowpage['page_type'], answer_column_content_id=answer_column_content_id, origin_answer_column_content_id=origin_answer_column_content_id, page_group=page_group_id, order=flowpage['order'])
  row = flow_page_model.MultipleTextQuestion(**new_multiple_text_question.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  flowpage_id = row.id
  
  # 解答欄と正答情報を追加
  print(f"**create_week*************{flowpage['correct_answers']}")
  for correct_answer in flowpage['correct_answers']:
    blank_name = correct_answer['blank_id']
    blank_id = await add_blank(db=db, blank_name=blank_name, flowpage_id=flowpage_id)
    for answer in correct_answer['answers']:
      await add_correct_answer(db=db, blank_id=blank_id, correct_answer=answer)
  return flowpage_id
  
async def add_descriptive_text_question(db: AsyncSession, content_id: int, hint_comment_id: int, answer_comment_id: int, origin_content_id: int, origin_hint_comment_id: int, origin_answer_comment_id: int, flowpage: dict, page_group_id: int):
  new_descriptive_text_question = flow_page_schema.DescriptiveTextQuestionCreate(content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, title=flowpage['title'], page_type=flowpage['page_type'], page_group=page_group_id, order=flowpage['order'])
  row = flow_page_model.DescriptiveTextQuestion(**new_descriptive_text_question.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  flowpage_id = row.id
  
  # 解答欄と正答情報を追加
  blank_name = 'blank_' + str(uuid.uuid4())
  blank_id = await add_blank(db=db, blank_name=blank_name, flowpage_id=flowpage_id)
  await add_correct_answer(db=db, blank_id=blank_id, correct_answer=flowpage['correct_answer'])
  return flowpage_id

async def add_choice_question(db: AsyncSession, content_id: int, hint_comment_id: int, answer_comment_id: int, origin_content_id: int, origin_hint_comment_id: int, origin_answer_comment_id: int, flowpage: dict, page_group_id: int):
  new_choice_question = flow_page_schema.ChoiceQuestionCreate(content_id=content_id, hint_comment_id=hint_comment_id, answer_comment_id=answer_comment_id, origin_content_id=origin_content_id, origin_hint_comment_id=origin_hint_comment_id, origin_answer_comment_id=origin_answer_comment_id, title=flowpage['title'], page_type=flowpage['page_type'], page_group=page_group_id, order=flowpage['order'])
  row = flow_page_model.ChoiceQuestion(**new_choice_question.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  flowpage_id = row.id
  
  # 選択肢情報の追加
  blank_name = 'blank_' + str(uuid.uuid4())
  blank_id = await add_blank(db=db, blank_name=blank_name, flowpage_id=flowpage_id)
  for choice_i, choice in enumerate(flowpage['choices']):
    await add_choice_question_choices(db=db, flowpage_id=flowpage_id, order=choice_i, choice=choice)

  # 正答情報の追加
  correct_answer = {'type': 'str', 'value': ",".join(sorted(flowpage['correct_choices']))}
  await add_correct_answer(db=db, blank_id = blank_id, correct_answer=correct_answer)
  
  return flowpage_id

async def add_choice_question_choices(db: AsyncSession, flowpage_id: int, order: int, choice: dict):
  content_id = await add_content(db=db, content=choice['choice_text'])
  new_choice_question_choices = flow_page_schema.ChoiceQuestionChoicesCreate(id=choice['choice_id'], flowpage_id=flowpage_id, order=order, content_id=content_id)
  row = flow_page_model.ChoiceQuestionChoice(**new_choice_question_choices.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return

async def add_block(db: AsyncSession, week_id: int, page: int, content_id: int, origin_content_id: int):
  new_block = block_schema.BlockCreate(week_id=week_id, page=page, content_id=content_id, origin_content_id=origin_content_id)
  row = block_model.Block(**new_block.dict())
  db.add(row)
  await db.flush()
  await db.refresh(row)
  return row.id

async def add_block_rules(db: AsyncSession, block_id: int, rules=None):
  new_block_rule = block_schema.BlockRuleCreate(block_id=block_id)
  if rules != None:
    if 'start_date_time' in rules:
      new_block_rule.start_date_time = rules['start_date_time']
    if 'end_date_time' in rules:
      new_block_rule.start_date_time = rules['end_date_time']
    if 'always' in rules:
      new_block_rule.start_date_time = rules['always']
    row = block_model.BlockRule(**new_block_rule.dict())
    db.add(row)
    return

async def get_data(db: AsyncSession, course_id: int):
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
  flows = flow_result.mappings().all()
  
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
  pages = page_result.mappings().all()
  
  return flows, pages

async def register_week(user_with_grant: user_schema.UserWithGrant, register_week_request: week_schema.RegisterWeekRequest, db: AsyncSession):
  flow_list, page_list = await get_data(db=db, course_id=register_week_request.course_id)
  yaml_formatter = YamlFormatter(register_week_request.week_files, flow_list, page_list)
  validate_result = yaml_formatter.validate_files()
  if validate_result['success']:
    return await add_week_file(db=db, user_with_grant=user_with_grant, register_week_request=register_week_request, block_yml_list=yaml_formatter.block_yml_list, flow_yml_list=yaml_formatter.flow_yml_list, image_dict=yaml_formatter.image_dict, flow_list=flow_list, page_list=page_list)
  return validate_result