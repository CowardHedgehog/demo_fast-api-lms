# フローページ情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DATETIME, TIME
from sqlalchemy.orm import relationship

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from api.db import Base

# フローページ情報
class FlowPage(Base):
  __tablename__ = 'flowpages'
  
  id = Column(Integer, primary_key=True, index=True, comment='問題ID')
  title = Column(String(128), nullable=False, comment='問題名')
  created = Column(DATETIME, default=datetime.now(ZoneInfo('Asia/Tokyo')))
  page_type = Column(String(128), nullable=False, comment='ページ種別')
  page_group = Column(Integer, ForeignKey('page_groups.id', ondelete='CASCADE'), nullable=False, comment='ページグループ')
  order = Column(Integer, nullable=False, comment='ページグループ内での順番')
  content_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, comment='問題コンテンツid')
  hint_comment_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, comment='ヒントコンテンツid')
  answer_comment_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, comment='解説コンテンツid')
  origin_content_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, comment='置換前の問題コンテンツ')
  origin_hint_comment_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, comment='置換前のヒントコンテンツ')
  origin_answer_comment_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, comment='置換前の解説コンテンツid')
  
# 解答欄情報
class Blank(Base):
  __tablename__ = 'blanks'
  
  id = Column(Integer, primary_key=True, index=True, comment='解答欄ID')
  blank_name = Column(String(256), comment='解答欄名')
  flowpage_id = Column(Integer, ForeignKey('flowpages.id', ondelete="CASCADE"), comment='対応するフローページ')
  
  question = relationship("Question", back_populates="blank")

# 解答機能を持つページ
class Question(FlowPage):
  __tablename__ = 'questions'
  
  id = Column(Integer, ForeignKey('flowpages.id'), primary_key=True)
  
  blank = relationship('Blank', back_populates='question')
  flowpage = relationship('FlowPage')
  
# 単一解答の問題を持つページ
class SingleTextQuestion(Question):
  __tablename__ = 'single_text_questions'
  
  id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
  
  question = relationship('Question')
  
# 複数解答の問題を持つページ
class MultipleTextQuestion(Question):
  __tablename__ = 'multiple_text_questions'
  
  id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
  answer_column_content_id = Column(Integer, ForeignKey('contents.id'), nullable=False)
  origin_answer_column_content_id = Column(Integer, ForeignKey('contents.id'), nullable=False)

  question = relationship('Question')
  
# 自由記述の問題を持つページ
class DescriptiveTextQuestion(Question):
  __tablename__ = 'descriptive_text_questions'
  
  id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
  
  question = relationship('Question')
  
# 選択式の問題を持つページ
class ChoiceQuestion(Question):
  __tablename__ = 'choice_questions'
  
  id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
  
  choice_question_choice = relationship('ChoiceQuestionChoice', back_populates='choice_question')
  question = relationship('Question')

# 選択式の問題の選択肢
class ChoiceQuestionChoice(Base):
  __tablename__ = 'choice_question_choices'
  
  id = Column(String(256), primary_key=True)
  flowpage_id = Column(Integer, ForeignKey("choice_questions.id"), primary_key=True)
  order = Column(Integer, nullable=False, comment="選択肢内での表示順序. 小さいものから順に表示される. 同じページ内で一意.")
  content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)

  choice_question = relationship("ChoiceQuestion", back_populates="choice_question_choice")

# 正答情報
class CorrectAnswer(Base):
  __tablename__ = 'correct_answers'
  
  id = Column(Integer, primary_key=True, index=True, comment='正答ID')
  blank_id = Column(Integer, ForeignKey('blanks.id', ondelete="CASCADE"), nullable=False, comment='対応する解答欄ID')
  type = Column(String(32), nullable=False, comment='解答の型')
  value = Column(String(256), nullable=False, comment='問題の正答')