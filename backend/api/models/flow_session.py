# フローセッション情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime as DATETIME, TIME, Float, TEXT
from sqlalchemy.orm import relationship

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from api.db import Base

# フローセッション情報
class FlowSession(Base):
  __tablename__ = 'flow_sessions'
  
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
  flow_id = Column(Integer, ForeignKey('flows.id', ondelete="CASCADE"), nullable=False)
  start_date_time = Column(DATETIME, comment='セッションを開始した日時')
  finish_date_time = Column(DATETIME, comment='セッションを終了した日時')
  is_finished = Column(Boolean, default=False, comment='セッションを終了したか')
  flow_session_grade = Column(Float, default=0.0, comment='正答率')

# フローセッションが持つ問題情報
class FlowSessionFlowPage(Base):
  __tablename__ = 'flow_session_flow_page'
  
  flow_session_id = Column(Integer, ForeignKey('flow_sessions.id', ondelete="CASCADE"), primary_key=True)
  flowpage_id = Column(Integer, ForeignKey('flowpages.id', ondelete="CASCADE"), primary_key=True)
  order = Column(Integer, nullable=False, comment='フローセッション内での表示順序')
  submitted = Column(Boolean, default=False, comment='問題を解答したか')
  is_correct = Column(Boolean, default=False, comment='解答が正解か')

# フローセッションと各ページの解答情報
class FlowSessionBlankAnswers(Base):
  __tablename__ = 'flow_session_blank_answer'
  
  id = Column(Integer, primary_key=True, index=True)
  flow_session_id = Column(Integer, ForeignKey('flow_sessions.id', ondelete="CASCADE"), nullable=False)
  flowpage_id = Column(Integer, ForeignKey('flowpages.id', ondelete="CASCADE"), nullable=False)
  blank_id = Column(Integer, ForeignKey('blanks.id', ondelete="CASCADE"), nullable=False)
  answer = Column(TEXT, comment='ユーザが解答した内容')
  created = Column(DATETIME, default=datetime.now(), nullable=False, comment='解答日時')
