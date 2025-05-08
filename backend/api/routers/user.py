from fastapi import APIRouter, Depends, HTTPException,status,Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from datetime import date
from api.db import get_db
import api.cruds.user as user_crud
import api.cruds.flow as flow_crud
import api.schemas.user as user_schema

router = APIRouter()

# ユーザ情報の取得
@router.get('/home_profile/', response_model = user_schema.HomeUserProfile, tags=['user'])
async def get_home_user_profile(user_profile = Depends(user_crud.get_home_profile)):
    return user_profile

# ユーザ一覧を取得する
@router.get('/get_users', response_model = List[user_schema.TakingUsersResponse], tags=['user'])
async def get_taking_users(user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.get_taking_users(db=db, user_id=user.id)

# week_id, flow_idから自身の能力値の取得
@router.get('/get_user_ability/{week_id}/{flow_id}', tags=['user'])
async def get_user_ability(week_id: int, flow_id: int, user: user_schema.User = Depends(user_crud.get_current_active_user), db: AsyncSession = Depends(get_db)):
    user_id = user.id
    user_ability = await user_crud.get_user_ability(db, week_id, flow_id, user_id)
    return user_ability

# ログイン後にユーザのパスワードを変更する
@router.post("/update_password", response_model=user_schema.UpdatePasswordResponse, tags=['user'])
async def update_password(update_password_request:user_schema.UpdatePasswordRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db:AsyncSession=Depends(get_db)):
    return await user_crud.update_password(db=db, user=user, update_password_request=update_password_request)

# ユーザ登録
@router.post('/add_user', response_model=user_schema.AddUsersResponse, tags=['user'])
async def add_user(add_user_request: user_schema.AddUserRequest, user_grant: user_schema.UserWithGrant=Depends(user_crud.get_user_grant), db: AsyncSession=Depends(get_db)):
    if not user_grant.create:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await user_crud.add_user(db, add_user_request)

# 複数ユーザ登録
@router.post('/add_users', tags=['user'])
async def add_users(add_user_request: List[user_schema.AddUserRequest], user_grant: user_schema.UserWithGrant=Depends(user_crud.get_user_grant), db: AsyncSession=Depends(get_db)):
    if not user_grant.create:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return await user_crud.add_users(db, add_user_request)

# アクセス履歴登録
@router.post('/add_access_history', tags=['test'])
async def add_access_history(add_access_history_request: user_schema.AddAccessHistoryRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.register_access_history(db=db, user=user, add_access_history_request=add_access_history_request)

# テーマカラーの登録
@router.post('/register_theme', tags = ['Top'])
async def register_theme(register_theme_request:user_schema.ThemeRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.register_theme(db, user.id, register_theme_request)
#テーマカラーの取得
@router.get('/get_theme', tags = ['Top'])
async def get_theme(user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.get_theme(db, user.id)

#ログイン日数の取得
@router.post('/login_num', tags = ['Top'])
async def login_num(user:user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession = Depends(get_db)):
    return await user_crud.register_login_num(db, user.id)

#ユーザー名の取得
@router.get('/user_name', tags = ['Top'])
async def user_name(user:user_schema.User = Depends(user_crud.get_current_active_user), db:AsyncSession = Depends(get_db)):
    return await user_crud.get_user_name(db, user.id)

#目標設定
@router.post('/add_goal', tags =['Top'])
async def add_goal(add_goal_request: user_schema.GoalRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.register_goals_history(db, user.id, add_goal_request)

#目標の取得
@router.get('/get_goal', tags = ['Top'])
async def get_goal(user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.get_goals(db, user.id)
#達成の切り替え
@router.post('/toggle_completed', tags = ['Top'])
async def toggle_completed(toggle_completed_request: user_schema.ToggleRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.toggle_completed(db,user.id, toggle_completed_request)

#未達成目標の取得
@router.get('/get_not_goal', tags = ['Top'])
async def get_not_goal(user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.get_not_goal(db, user.id)
#目標の削除
@router.delete('/delete_goal', tags = ['Top'])
async def delete_goal(delete_request:user_schema.GoalDeleteRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.delete_goal(db, user.id, delete_request)
#進捗率の取得
@router.get('/get_progress/{course_id}', tags = ['Top'])
async def get_progress(course_id : int, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await flow_crud.flow_session_finished(db, user.id, course_id)

#所持ポイントの取得
@router.get('/get_point',tags = ['Top'])
async def get_point(user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.get_point(db,user.id)
#ポイントが高い人を取得
@router.get('/get_high_pointer', tags = ['Top'])
async def get_high_pointer(user: user_schema.User=Depends(user_crud.get_current_active_user),db: AsyncSession=Depends(get_db)):
    return await user_crud.get_high_pointer(db)
#ニックネームの設定
@router.post('/set_nickname', tags = ['Top'])
async def set_nickname(set_nickname_request: user_schema.SetNicknameRequest, user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.set_nickname(db, user.id, set_nickname_request)
#ニックネームの取得
@router.get('/get_nickname', tags = ['Top'])
async def get_nickname(user: user_schema.User=Depends(user_crud.get_current_active_user), db: AsyncSession=Depends(get_db)):
    return await user_crud.get_nickname(db, user.id)