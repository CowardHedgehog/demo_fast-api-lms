# フロー情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime as DATETIME, TIME
from sqlalchemy.orm import relationship

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from api.db import Base

# フロー情報
class Flow(Base):
  __tablename__ = 'flows'
  
  id = Column(Integer, primary_key=True, index=True, comment='演習問題ID')
  id_in_yml = Column(String(256), nullable=False, comment='yml内でのid')
  week_id = Column(Integer, ForeignKey('weeks.id', ondelete='CASCADE'), nullable=False, comment='対応するweek_id')
  title = Column(String(128), nullable=False, comment='演習問題名')
  created = Column(DATETIME, default=datetime.now())
  welcome_page_content_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, comment='演習前コンテンツid')
  completion_page_content_id = Column(Integer, ForeignKey('contents.id', ondelete='CASCADE'), nullable=False, comment='演習後コンテンツid')

# フロールール
class FlowRule(Base):
  __tablename__ = 'flow_rules'
  
  flow_id = Column(Integer, ForeignKey('flows.id', ondelete='CASCADE'), primary_key=True)
  check_answer_timing = Column(String(32), default='submit_page', comment='答え合わせするタイミング．["None", "submit_page", "end_of_flow"]')
  challenge_limit = Column(Integer, comment='挑戦できる回数')
  restart_session = Column(Boolean, default=True, nullable=False, comment='中断したセッションのリスタートできるか')
  time_limit = Column(TIME, comment='Flowの制限時間を設定する')
  start_date_time = Column(DATETIME, comment='Flowの表示を開始する日時．')
  end_answer_date_time = Column(DATETIME, comment='Flowの表示を終了する日時．')
  end_read_date_time = Column(DATETIME, comment='Flowの閲覧を終了する日時')
  always = Column(Boolean, default=True, comment='このFlowを常に表示するか')
  
# ユーザに対するフロー権限
class FlowGrant(Base):
  __tablename__ = 'flow_grant'
  
  user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
  flow_id = Column(Integer, ForeignKey('flows.id', ondelete='CASCADE'), primary_key=True)
  start_date_time = Column(DATETIME, nullable=False, comment='権限が有効になる日時')
  end_date_time = Column(DATETIME, nullable=False, comment='権限が無効になる日時')
  read_answer = Column(Boolean, default=False, nullable=False, comment='読取権限')
  update_answer = Column(Boolean, default=False, nullable=False, comment='更新権限')
  delete_answer = Column(Boolean, default=False, nullable=False, comment='削除権限')