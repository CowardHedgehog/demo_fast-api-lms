# yamlで書かれたコンテンツを格納するテーブル
from sqlalchemy import Column, Integer, DateTime as DATETIME, TEXT
from datetime import datetime

from api.db import Base

# コンテンツ情報
class Content(Base):
  __tablename__ = 'contents'
  
  id = Column(Integer, primary_key=True, index=True, comment='コンテンツに自動的に割り振られるID')
  content = Column(TEXT, nullable=False, comment='yaml内のコンテンツを格納')
  created = Column(DATETIME, default=datetime.now(), nullable=False, comment='コンテンツを登録した日時')
  last_updated = Column(DATETIME, default=datetime.now(), nullable=False, comment='コンテンツの最終更新日時')