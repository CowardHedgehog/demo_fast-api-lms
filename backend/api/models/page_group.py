# ページグループ情報を示すテーブル群
from sqlalchemy import Column, Integer, String, ForeignKey
from api.db import Base

class PageGroup(Base):
  __tablename__ = 'page_groups'
  
  id = Column(Integer, primary_key=True, index=True, comment='ページのまとまり')
  group_name = Column(String(128), nullable=False, comment='グループ名(ymlで入力)')
  flow_id = Column(Integer, ForeignKey('flows.id', ondelete='CASCADE'), nullable=False, comment='対応するFlow')
  order = Column(Integer, nullable=False, comment='Flowの中での順番')