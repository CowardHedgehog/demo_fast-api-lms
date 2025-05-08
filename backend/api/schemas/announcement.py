from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class AnnouncementBase(BaseModel):
    title: str
    content: str
    start_date_time: datetime
    end_date_time: datetime
    user_kind_id: int

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementCreateResponse(BaseModel):
    success: bool
    error_msg: str = ""
    announcement_id: Optional[int] = None

class Announcement(AnnouncementBase):
    id: int
    sender: str
    send_date_time: datetime

    class Config:
        orm_mode = True

class UserAnnouncementBase(BaseModel):
    user_id: int
    announcement_id: int

class UserAnnouncementCreate(UserAnnouncementBase):
    is_read: bool = False
    read_date_time: Optional[datetime] = None

class UserAnnouncement(UserAnnouncementBase):
    id: int
    is_read: bool
    read_date_time: Optional[datetime]

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    user_kind_id: int

    class Config:
        from_attributes = True  # Pydantic v2ではorm_modeの代わりにfrom_attributesを使用

class AnnouncementLogBase(BaseModel):
    user_id: int
    announcement_id: int
    action: str
    action_date_time: datetime

class AnnouncementLogCreate(AnnouncementLogBase):
    pass

class AnnouncementLog(AnnouncementLogBase):
    id: int

    class Config:
        orm_mode = True

class GetAnnouncementsResponse(BaseModel):
    announcements: List[Announcement]
    total_count: int
    unread_count: int

class AnnouncementUpdate(BaseModel):
    title: str
    content: str
    start_date_time: datetime
    end_date_time: datetime
    user_kind_id: int

class AnnouncementDelete(BaseModel):
    id: int

class AnnouncementDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    start_date_time: datetime
    end_date_time: datetime
    sender: str
    send_date_time: datetime
    user_kind_id: int
    is_read: bool
    is_active: bool
    total_read_count: int = 0

    class Config:
        from_attributes = True