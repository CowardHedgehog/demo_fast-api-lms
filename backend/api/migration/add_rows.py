from sqlalchemy.ext.asyncio import AsyncSession

from api.migration.m001_add_user_kind import add_user_kind
from api.migration.m002_add_user import add_user
from api.migration.m003_add_subject import add_subject
from api.migration.m004_add_subject_info_syllabus import add_subject_info_syllabus
from api.migration.m005_add_course import add_course
from api.migration.m006_add_taking_course import add_taking_course
#from api.migration.m007_add_course_grant import add_course_grant
from api.migration.m008_add_week import add_week
from api.migration.m009_add_content import add_content
from api.migration.m010_add_block import add_block
from api.migration.m011_add_flow import add_flow
from api.migration.m012_add_flow_rule import add_flow_rule
from api.migration.m013_add_page_group import add_page_group
from api.migration.m014_add_single_text_questions import add_single_text_questions
from api.migration.m015_add_multiple_text_question import add_multiple_text_question
from api.migration.m016_add_descriptive_text_question import add_descriptive_text_question
from api.migration.m017_add_choice_question import add_choice_question
from api.migration.m018_add_choice_question_choice import add_choice_question_choice
from api.migration.m019_add_blank import add_blank
from api.migration.m020_add_correct_answers import add_correct_answer

def add_rows(db: AsyncSession):
  add_user_kind(db)
  add_user(db)
  add_subject(db)
  add_subject_info_syllabus(db)
  add_course(db)
  add_taking_course(db)
  #add_course_grant(db)
  add_week(db)
  add_content(db)
  add_block(db)
  add_flow(db)
  add_flow_rule(db)
  add_page_group(db)
  add_single_text_questions(db)
  add_multiple_text_question(db)
  add_descriptive_text_question(db)
  add_choice_question(db)
  add_choice_question_choice(db)
  add_blank(db)
  add_correct_answer(db)
  
  db.commit()