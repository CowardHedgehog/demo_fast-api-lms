# ブロック情報（コース内の要素）を示すテーブル群
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime as DATETIME

from api.db import Base

# ブロック情報（各週とコンテンツの繋がり）
class Block(Base):
  __tablename__ = 'blocks'
  
  id = Column(Integer, primary_key=True, index=True, comment='block_id')
  week_id = Column(Integer, ForeignKey('weeks.id', ondelete="CASCADE"), nullable=False, comment='対応するweek_id')
  page = Column(Integer, nullable=False, comment='コンテンツのページ番号')
  content_id = Column(Integer, ForeignKey('contents.id', ondelete="CASCADE"), nullable=False, comment='対応するcontent_id')
  origin_content_id = Column(Integer, ForeignKey('contents.id', ondelete="CASCADE"), nullable=False, comment='置換前のcontent_id')
  
class BlockRule(Base):
  __tablename__ = 'block_rules'
  
  block_id = Column(Integer, ForeignKey('blocks.id'), primary_key=True)
  start_date_time = Column(DATETIME, comment='Blockの表示を開始する日時')
  end_date_time = Column(DATETIME, comment='Blockの表示を終了する日時')
  always = Column(Boolean, default=True, nullable=True, comment='このBlockを常に表示するか')