# 科目情報を示すテーブル
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime as DATETIME, TEXT
from sqlalchemy.orm import relationship
import datetime
from api.db import Base

# 科目情報
class Subject(Base):
  __tablename__ = 'subjects'
  
  id = Column(Integer, primary_key=True, index=True, comment='科目ID')
  subject_name = Column(String(256), nullable=False, comment='科目名')
  period = Column(String(256), nullable=False, comment='開講時期')
  created = Column(DATETIME, default=datetime.datetime.now(), nullable=False, comment='作成日時')
  created_by = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, comment='作成者')
  is_active = Column(Boolean, default=True, nullable=False, comment='有効化')

# 科目のシラバス情報
class SubjectInfoSyllabus(Base):
  __tablename__ = 'subject_info_syllubus'
  
  subject_id = Column(Integer, ForeignKey('subjects.id', ondelete="CASCADE"), primary_key=True, comment='科目ID')
  subject_class = Column(String(128), nullable=False, comment='授業科目区分')
  subject_credit = Column(Integer, nullable=False, comment='単位')
  subject_code = Column(String(128), nullable=False, comment='科目コード')
  subject_keyword = Column(TEXT, nullable=False, comment='キーワード')
  subject_goals = Column(TEXT, nullable=False, comment='学習・教育目標')
  
  subject = relationship('Subject')