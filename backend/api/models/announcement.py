from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DATETIME
from sqlalchemy.orm import relationship
import datetime
from zoneinfo import ZoneInfo

from api.db import Base

class Announcement(Base):
    __tablename__ = 'announcements'
    
    id = Column(Integer, primary_key=True, index=True, comment='お知らせID')
    title = Column(String(255), nullable=False, comment='お知らせタイトル')
    content = Column(Text, nullable=False, comment='お知らせ内容')
    start_date_time = Column(DATETIME, nullable=False, comment='表示開始日時')
    end_date_time = Column(DATETIME, nullable=False, comment='表示終了日時')
    sender = Column(String(255), nullable=False, comment='送信者')
    send_date_time = Column(DATETIME, default=datetime.datetime.now(ZoneInfo('Asia/Tokyo')), nullable=False, comment='送信日時')
    user_kind_id = Column(Integer, ForeignKey('user_kind.id'), nullable=False, comment='ユーザーの種類ID')
    is_active = Column(Boolean, default=True, nullable=False)


class UserAnnouncement(Base):
    __tablename__ = 'user_announcements'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    announcement_id = Column(Integer, ForeignKey('announcements.id', ondelete="CASCADE"), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    read_date_time = Column(DATETIME, nullable=True)
    
    user = relationship('User')
    announcement = relationship('Announcement')

class AnnouncementLog(Base):
    __tablename__ = 'announcement_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    announcement_id = Column(Integer, ForeignKey('announcements.id', ondelete="CASCADE"), nullable=False)
    action = Column(String(50), nullable=False)
    action_date_time = Column(DATETIME, default=datetime.datetime.now(ZoneInfo('Asia/Tokyo')), nullable=False)
    
    user = relationship('User')
    announcement = relationship('Announcement') 