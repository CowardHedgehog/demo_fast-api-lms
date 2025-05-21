from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, update, delete, func
from sqlalchemy.engine import Result
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Optional, Union
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload, joinedload  # 必要に応じてインポート

import api.models.announcement as announcement_model
import api.models.user as user_model
import api.schemas.announcement as announcement_schema
import api.schemas.user as user_schema

async def get_target_users(
    db: AsyncSession,
    user_kind_id: int
) -> List[int]:
    query = select(user_model.User).options(
        selectinload(user_model.User.user_kind)
    ).where(
        user_model.User.is_active == True,
        user_model.User.user_kind_id == user_kind_id
    )
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    # user_idのリストを返す
    return [user.id for user in users]

async def create_announcement(
    db: AsyncSession, 
    announcement: announcement_schema.AnnouncementCreate,
    user: user_schema.User
) -> announcement_schema.AnnouncementCreateResponse:
    try:
        new_announcement = announcement_model.Announcement(
            title=announcement.title,
            content=announcement.content,
            start_date_time=announcement.start_date_time,
            end_date_time=announcement.end_date_time,
            sender=user.username,
            send_date_time=datetime.now(),
            user_kind_id=announcement.user_kind_id
        )
        
        db.add(new_announcement)
        await db.flush()
        
        # 対象ユーザーの取得
        target_users = await get_target_users(db, announcement.user_kind_id)
        
        # ユーザーのお知らせ追加
        user_announcements = [
            announcement_model.UserAnnouncement(
                user_id=target_user,
                announcement_id=new_announcement.id,
                is_read=False
            )
            for target_user in target_users
        ]
        
        db.add_all(user_announcements)
        await db.commit()
        await db.refresh(new_announcement)
        
        return announcement_schema.AnnouncementCreateResponse(
            success=True,
            announcement_id=new_announcement.id
        )
    except Exception as e:
        await db.rollback()
        print(f"Error occurred: {str(e)}")
        return announcement_schema.AnnouncementCreateResponse(
            success=False,
            error_msg=str(e)
        )
    

async def get_announcements(
    db: AsyncSession,
    user: user_schema.User,
    limit: int = 10,
    offset: int = 0
) -> announcement_schema.GetAnnouncementsResponse:
    current_time = datetime.now()
    
    result: Result = await db.execute(
        select(announcement_model.Announcement)
        .join(announcement_model.UserAnnouncement)
        .where(
            and_(
                announcement_model.UserAnnouncement.user_id == user.id,
                announcement_model.Announcement.start_date_time <= current_time,
                announcement_model.Announcement.end_date_time >= current_time
            )
        )
        .order_by(announcement_model.Announcement.send_date_time.desc())
        .offset(offset)
        .limit(limit)
    )
    announcements = result.scalars().all()

    # 総件数と未読件数の取得
    count_result = await db.execute(
        select(
            announcement_model.UserAnnouncement.id,
            announcement_model.UserAnnouncement.is_read
        ).where(announcement_model.UserAnnouncement.user_id == user.id)
    )
    user_announcements = count_result.all()
    total_count = len(user_announcements)
    unread_count = len([ua for ua in user_announcements if not ua.is_read])

    return announcement_schema.GetAnnouncementsResponse(
        announcements=announcements,
        total_count=total_count,
        unread_count=unread_count
    )

async def mark_as_read(
    db: AsyncSession,
    user_id: int,
    announcement_id: int
) -> bool:
    try:
        result = await db.execute(
            update(announcement_model.UserAnnouncement)
            .where(
                and_(
                    announcement_model.UserAnnouncement.user_id == user_id,
                    announcement_model.UserAnnouncement.announcement_id == announcement_id
                )
            )
            .values(
                is_read=True,
                read_date_time=datetime.now()
            )
        )
        if result.rowcount == 0:
            print("No rows were updated. Check if the user_id and announcement_id are correct.")
            return False

        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        print(f"Error occurred: {str(e)}")
        return False

async def update_announcement(
    db: AsyncSession,
    announcement_id: int,
    announcement: announcement_schema.AnnouncementUpdate,
    user: user_schema.User
) -> bool:
    try:
        # 既存のお知らせを無効化
        await db.execute(
            update(announcement_model.Announcement)
            .where(announcement_model.Announcement.id == announcement_id)
            .values(is_active=False)
        )

        # 新しいお知らせを作成
        new_announcement_response = await create_announcement(db, announcement, user)
        
        if not new_announcement_response.success:
            raise Exception(new_announcement_response.error_msg)

        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        print(f"Error occurred: {str(e)}")
        return False

async def delete_announcement(
    db: AsyncSession,
    announcement_id: int,
    user: user_schema.User
) -> bool:
    try:
        # お知らせを削除する代わりに、is_activeをFalseに設定
        await db.execute(
            update(announcement_model.Announcement)
            .where(announcement_model.Announcement.id == announcement_id)
            .values(is_active=False)
        )
        await db.commit()
        return True
    except:
        await db.rollback()
        return False

async def get_announcement_detail(
    db: AsyncSession,
    announcement_id: int,
    user: user_schema.User
) -> Optional[announcement_schema.AnnouncementDetailResponse]:
    try:
        # お知らせの取得
        result = await db.execute(
            select(announcement_model.Announcement)
            .where(announcement_model.Announcement.id == announcement_id)
        )
        announcement = result.scalar_one_or_none()
        
        if not announcement:
            return None

        # ユーザーの既読状態を取得
        user_announcement_result = await db.execute(
            select(announcement_model.UserAnnouncement)
            .where(
                and_(
                    announcement_model.UserAnnouncement.announcement_id == announcement_id,
                    announcement_model.UserAnnouncement.user_id == user.id
                )
            )
        )
        user_announcement = user_announcement_result.scalar_one_or_none()

        # 総既読数を取得
        total_read_count_result = await db.execute(
            select(func.count())
            .select_from(announcement_model.UserAnnouncement)
            .where(
                and_(
                    announcement_model.UserAnnouncement.announcement_id == announcement_id,
                    announcement_model.UserAnnouncement.is_read == True
                )
            )
        )
        total_read_count = total_read_count_result.scalar_one()

        return announcement_schema.AnnouncementDetailResponse(
            id=announcement.id,
            title=announcement.title,
            content=announcement.content,
            start_date_time=announcement.start_date_time,
            end_date_time=announcement.end_date_time,
            sender=announcement.sender,
            send_date_time=announcement.send_date_time,
            user_kind_id=announcement.user_kind_id,
            is_read=user_announcement.is_read if user_announcement else False,
            total_read_count=total_read_count
        )
    except Exception as e:
        await db.rollback()
        print(f"Error occurred: {str(e)}")
        return None
