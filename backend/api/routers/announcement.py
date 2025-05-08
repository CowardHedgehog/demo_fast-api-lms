from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy import select

import api.cruds.announcement as announcement_crud
import api.cruds.user as user_crud
import api.schemas.announcement as announcement_schema
import api.schemas.user as user_schema
from api.db import get_db
from api.models.announcement import Announcement as AnnouncementModel
import api.models.announcement as announcement_model

router = APIRouter()

@router.post("/announcements", response_model=announcement_schema.AnnouncementCreateResponse, tags=['announcement'])
async def create_announcement(
    announcement: announcement_schema.AnnouncementCreate,
    user: user_schema.UserWithGrant = Depends(user_crud.get_user_grant),
    db: AsyncSession = Depends(get_db)
):
    """
    お知らせを新規作成するためのエンドポイント
    """
    if not user.create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません"
        )
    return await announcement_crud.create_announcement(db, announcement, user)


@router.get("/announcements/{user_kind_id}", response_model=List[int], tags=['announcement'])
async def get_target_users(
    user_kind_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたユーザー種別のユーザーIDを取得するためのエンドポイント
    """
    return await announcement_crud.get_target_users(db, user_kind_id)

@router.get("/announcements_list", response_model=List[announcement_schema.AnnouncementDetailResponse], tags=['announcement'])
async def get_user_announcements(
    user: user_schema.User = Depends(user_crud.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    認証されたユーザーへのお知らせとその内容を取得するエンドポイント
    """
    try:
        # ユーザーに関連するお知らせを取得
        result = await db.execute(
            select(announcement_model.Announcement, announcement_model.UserAnnouncement.is_read)
            .join(announcement_model.UserAnnouncement)
            .where(
                announcement_model.UserAnnouncement.user_id == user.id
            )
            .order_by(announcement_model.Announcement.send_date_time.desc())
        )
        announcements = result.all()

        # お知らせの詳細をリストとして返す
        announcement_details = [
            announcement_schema.AnnouncementDetailResponse(
                id=announcement.Announcement.id,
                title=announcement.Announcement.title,
                content=announcement.Announcement.content,
                start_date_time=announcement.Announcement.start_date_time,
                end_date_time=announcement.Announcement.end_date_time,
                sender=announcement.Announcement.sender,
                send_date_time=announcement.Announcement.send_date_time,
                user_kind_id=announcement.Announcement.user_kind_id,
                is_read=announcement.is_read,
                is_active=announcement.Announcement.is_active,
                total_read_count=0
            )
            for announcement in announcements
        ]

        return announcement_details
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred: {str(e)}"
        )

@router.post("/announcements/{announcement_id}/read", tags=['announcement'])
async def mark_as_read(
    announcement_id: int,
    user: user_schema.User = Depends(user_crud.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたお知らせを既読にするためのエンドポイント
    """
    result = await announcement_crud.mark_as_read(db, user.id, announcement_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="既読処理に失敗しました"
        )
    return {"success": True}

@router.put("/announcements/{announcement_id}", tags=['announcement'])
async def update_announcement(
    announcement_id: int,
    announcement: announcement_schema.AnnouncementUpdate,
    user: user_schema.UserWithGrant = Depends(user_crud.get_user_grant),
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたお知らせのis_activeをfalseにして、新しいお知らせとして作成するエンドポイント
    """
    if not user.create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません"
        )

    # 修正: announcement_idをupdate_announcement関数に渡す
    result = await announcement_crud.update_announcement(db, announcement_id, announcement, user)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新に失敗しました"
        )
    return {"success": True}

@router.delete("/announcements/{announcement_id}", tags=['announcement'])
async def delete_announcement(
    announcement_id: int,
    user: user_schema.UserWithGrant = Depends(user_crud.get_user_grant),
    db: AsyncSession = Depends(get_db)
):
    """
    指定されたお知らせのis_activeをfalseにして、削除するエンドポイント
    """
    if not user.create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません"
        )
    result = await announcement_crud.delete_announcement(db, announcement_id, user)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="削除に失敗しました"
        )
    return {"success": True}

@router.get("/announcements_detail/{announcement_id}", response_model=announcement_schema.AnnouncementDetailResponse, tags=['announcement'])
async def get_announcement_detail(
    announcement_id: int,
    user: user_schema.User = Depends(user_crud.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await announcement_crud.get_announcement_detail(db, announcement_id, user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="お知らせが見つかりません"
        )
    return result 

@router.get("/announcements_list_all", response_model=List[announcement_schema.AnnouncementDetailResponse], tags=['announcement'])
async def get_all_active_announcements(
    user: user_schema.UserWithGrant = Depends(user_crud.get_user_grant),
    db: AsyncSession = Depends(get_db)
):
    """
    is_activeがtrueの全てのお知らせを取得するエンドポイント
    """
    try:
        # is_activeがtrueの全てのお知らせを取得
        result = await db.execute(
            select(announcement_model.Announcement)
            .where(announcement_model.Announcement.is_active == True)
            .order_by(announcement_model.Announcement.send_date_time.desc())
        )
        announcements = result.scalars().all()  # scalars()を追加

        # お知らせの詳細をリストとして返す
        announcement_details = [
            announcement_schema.AnnouncementDetailResponse(
                id=announcement.id,
                title=announcement.title,
                content=announcement.content,
                start_date_time=announcement.start_date_time,
                end_date_time=announcement.end_date_time,
                sender=announcement.sender,
                send_date_time=announcement.send_date_time,
                user_kind_id=announcement.user_kind_id,
                is_read=False,  # 管理画面用なので固定値
                is_active=announcement.is_active,  # is_activeフィールドを追加
                total_read_count=0  # 管理画面用なので固定値
            )
            for announcement in announcements
        ]

        return announcement_details
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred: {str(e)}"
        )
