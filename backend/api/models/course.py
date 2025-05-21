# コース情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime as DATETIME, TEXT
from sqlalchemy.orm import relationship

import datetime
from zoneinfo import ZoneInfo

from api.db import Base

# コース情報
class Course(Base):
  __tablename__ = 'courses'
  
  id = Column(Integer, primary_key=True, index=True, comment='コースID')
  subject_id = Column(Integer, ForeignKey('subjects.id', ondelete="CASCADE"), nullable=False, comment='科目ID')
  course_name = Column(String(128), nullable=False, comment='コース名')
  weeks = Column(Integer, nullable=False, comment='週数')
  start_date_time = Column(DATETIME, nullable=False, comment='開始日時')
  end_date_time = Column(DATETIME, nullable=False, comment='終了日時')
  created = Column(DATETIME,default=datetime.datetime.now(), nullable=False, comment='作成日時')
  created_by = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, comment='作成者')
  is_active = Column(Boolean, default=True, nullable=False, comment='コース有効化')
  
  subject = relationship('Subject')
  
# コース解答の閲覧権限情報
class CourseGrant(Base):
  __tablename__ = "course_grant"

  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
  start_date_time = Column(DATETIME, nullable=False, comment="権限が有効になる日時.")
  end_date_time = Column(DATETIME, nullable=False, comment="権限が失効する日時")
  read_answer = Column(Boolean, default=False, nullable=False, comment="読取権限.")
  update_answer = Column(Boolean, default=False, nullable=False, comment="更新権限")
  delete_answer = Column(Boolean, default=False, nullable=False, comment="削除権限")
    
# コース履修情報
class TakingCourse(Base):
  __tablename__ = "taking_course"

  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)

  user = relationship("User")
  course = relationship("Course")