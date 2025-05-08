from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey

from api.db import Base

class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(30), nullable=True, comment="画像ファイル名.")
    week_id = Column(Integer, ForeignKey('weeks.id', ondelete="CASCADE"), comment='week_content登録時に画像がある場合、week_idを保持しておく')
    imgdata = Column(LargeBinary(length=(2**32)-1),nullable=True)