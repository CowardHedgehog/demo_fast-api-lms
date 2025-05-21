# 週情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime as DATETIME, TEXT
from sqlalchemy.orm import relationship

import datetime
from zoneinfo import ZoneInfo

from api.db import Base

# 各週（各回）のコンテンツ情報
class Week(Base):
  __tablename__ = 'weeks'
  
  id = Column(Integer, primary_key=True, index=True, comment='WeekID')
  course_id = Column(Integer, ForeignKey('courses.id', ondelete="CASCADE"), nullable=False, comment='コースID')
  week_name = Column(String(128), nullable=False, comment='Week名')
  week_num = Column(Integer, nullable=False, comment='第〇週, 第〇回')
  order = Column(Integer, default=1, nullable=False, comment='並び順（同週内）')
  created = Column(DATETIME, default=datetime.datetime.now(), nullable=False, comment='作成日時')
  created_by = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, comment='作成者')
  is_active = Column(Boolean, default=True, nullable=False, comment='週有効化')
  
  course = relationship('Course')