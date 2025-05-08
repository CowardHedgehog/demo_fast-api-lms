from fastapi import  Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update,func,desc,delete
from typing import List, Optional
from jose import JWTError, jwt
import datetime
from zoneinfo import ZoneInfo

from api.db import get_db
from api.cruds.domains.generate_hash import verify_password, get_password_hash
from api.schemas.token import TokenData
import api.schemas.user as user_schema
import api.models.user as user_model
import api.models.course as course_model


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'

async def authenticate_user(db: AsyncSession, email: str, password: str):
  user = await select_user(db, email)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user

async def select_user(db: AsyncSession, email: str) -> List[user_schema.User]:
  result: Result = await(
    db.execute(
      select(
        user_model.User.id,
        user_model.User.username,
        user_model.User.email,
        user_model.User.hashed_password,
        user_model.User.user_kind_id,
        user_model.User.created,
        user_model.User.is_active,
      ).where(user_model.User.email == email)
    )
  )
  return result.first()

async def select_users(db: AsyncSession) -> List[user_schema.TakingUsersResponse]:
  result: Result = await(
    db.execute(
      select(
        user_model.User.id,
        user_model.User.username,
        user_model.User.email,
        user_model.UserKind.kind_name
      ).where(user_model.User.user_kind_id == user_model.UserKind.id)
    )
  )
  return result.all()

async def select_user_kind(db: AsyncSession):
  result: Result = await(
    db.execute(
      select(
        user_model.UserKind.kind_name,
        user_model.UserKind.id
      )
    )
  )
  return result.all()

async def select_user_profile(db: AsyncSession, email: str) -> user_schema.HomeUserProfile:
  result: Result = await(
    db.execute(
      select(
        user_model.User.username,
        user_model.User.email,
        user_model.User.is_active,
        user_model.UserKind.kind_name,
        user_model.UserKind.create
      ).where(user_model.User.email == email)
      .where(user_model.User.user_kind_id == user_model.UserKind.id)
    )
  )
  return result.mappings().first()

async def select_user_ability(db: AsyncSession, week_id: int, flow_id: int, user_id: int) -> user_schema.UserAbilityResponse:
  result: Result = await(
    db.execute(
      select(
        user_model.IrtAbility.ability
      ).where(user_model.IrtAbility.week_id == week_id)
      .where(user_model.IrtAbility.flow_id == flow_id)
      .where(user_model.IrtAbility.user_id == user_id)
    )
  )
  user_ability = result.first()
  return user_ability[0]

async def select_user_with_grant(db: AsyncSession,email: str) -> List[user_schema.UserWithGrant]:
  result: Result = await(
    db.execute(
      select(
        user_model.User.id,
        user_model.User.username,
        user_model.User.email,
        user_model.User.created,
        user_model.User.is_active,
        user_model.UserKind.kind_name,
        user_model.UserKind.create
      ).where(user_model.User.email == email)
      .where(user_model.User.user_kind_id == user_model.UserKind.id)
    )
  )
  # print(result.all())
  return result.first()

async def select_access_history(db: AsyncSession, user: user_schema.User, add_access_history_request: user_schema.AddAccessHistoryRequest):
  print(add_access_history_request)
  result: Result = await(
    db.execute(
      select(
        user_model.AccessHistory.time
      ).where(user_model.AccessHistory.user_id == user.id)
      .where(user_model.AccessHistory.date == add_access_history_request.date)
      .where(user_model.AccessHistory.page == add_access_history_request.page)
      .where(user_model.AccessHistory.details == add_access_history_request.details)
    )
  )
  return result.mappings().first()

async def add_access_history(db: AsyncSession, user: user_schema.User, add_access_history_request: user_schema.AddAccessHistoryRequest):
  new_access_history = user_schema.AddAccessHistory(user_id=user.id, date=add_access_history_request.date, time=add_access_history_request.time, page=add_access_history_request.page, details=add_access_history_request.details)
  row = user_model.AccessHistory(**new_access_history.dict())
  db.add(row)
  await db.flush()
  return 'success'

async def update_access_history(db: AsyncSession, user: user_schema.User, add_access_history_request: user_schema.AddAccessHistoryRequest, access_time: int):
  result: Result = await(
    db.execute(
      update(user_model.AccessHistory)
      .where(user_model.AccessHistory.user_id == user.id)
      .where(user_model.AccessHistory.date == add_access_history_request.date)
      .where(user_model.AccessHistory.page == add_access_history_request.page)
      .where(user_model.AccessHistory.details == add_access_history_request.details)
      .values(time=add_access_history_request.time+access_time)
    )
  )
  await db.flush()
  return 'success'
  




async def update_password(db: AsyncSession, user: user_schema.User, update_password_request: user_schema.UpdatePasswordRequest) -> user_schema.UpdatePasswordResponse:
  if not verify_password(update_password_request.old_password, user.hashed_password):
    return {'success': False, 'email': update_password_request.email, 'error_msg': '現在のパスワードが間違っています', 'password': update_password_request.old_password}
  new_hashed_password = get_password_hash(update_password_request.new_password)
  result :Result = await(
    db.execute(
      update(user_model.User)
      .where(user_model.User.id == user.id)
      .values(hashed_password = new_hashed_password)
    )
  )
  await db.commit()
  return {'success': True, 'email': update_password_request.email, 'error_msg': '', 'password': update_password_request.new_password}

async def get_token(token: Optional[str] = Cookie(None)):
  return token

async def get_home_profile(db: AsyncSession = Depends(get_db), token: Optional[str] = Depends(get_token)):
  credentials_exception = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Could not validate credentials',
    headers = {'WWW-Authenticate': 'Bearer'}
  )
  try:
    if token == None:
      raise credentials_exception
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    email: str = payload.get('sub')
    if email is None:
      raise credentials_exception
    token_data = TokenData(email = email)
  except JWTError:
    raise credentials_exception
  user_profile = await select_user_profile(db, email = token_data.email)
  if user_profile is None:
    raise credentials_exception
  return user_profile

async def get_authed_token(token = Depends(get_token)):
  credentials_exception = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Could not validate credentials',
    headers = {'WWW-Authenticate': 'Bearer'}
  )
  try:
    if token == None:
      raise credentials_exception
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    email: str = payload.get('sub')
    if email is None:
      raise credentials_exception
    token_data = TokenData(email = email)
    return token_data
  except JWTError:
    raise credentials_exception

async def get_taking_users(db: AsyncSession, user_id: int):
  return await select_users(db=db)

async def get_current_user(db: AsyncSession = Depends(get_db), token: Optional[str] = Depends(get_token)):
  credentials_exception = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = 'Could not validate credentials',
    headers = {'WWW-Authenticate': 'Bearer'}
  )
  try:
    if token == None:
      raise credentials_exception
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    email: str = payload.get('sub')
    if email is None:
      raise credentials_exception
    token_data = TokenData(email = email)
  except JWTError:
    raise credentials_exception
  user = await select_user(db, email = token_data.email)
  if user is None:
    raise credentials_exception
  return user

async def get_current_active_user(current_user: user_schema.User = Depends(get_current_user)):
  if not current_user.is_active:
    raise HTTPException(status_code = 400, detail = 'Inactive user')
  return current_user

async def get_user_with_grant(db: AsyncSession = Depends(get_db),token: Optional[str] = Depends(get_token)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    if token == None:
      raise credentials_exception
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
    token_data = TokenData(email=email)

  except JWTError:
    raise credentials_exception
  user_with_grant = await select_user_with_grant(db, email=token_data.email)
  if user_with_grant is None:
    raise credentials_exception
  return user_with_grant

async def get_user_grant(current_user: user_schema.UserWithGrant = Depends(get_user_with_grant)):
  if not current_user.is_active:
    raise HTTPException(status_code=400, detail="Inactive user")
  elif not current_user.create:
    raise HTTPException(status_code=400, detail="Inactive user")
  return current_user

async def get_user_ability(db: AsyncSession, week_id: int, flow_id: int, user_id: int):
  user_ability = await select_user_ability(db = db, week_id = week_id, flow_id = flow_id, user_id = user_id)
  return user_ability

async def add_user(db: AsyncSession, add_user_request: user_schema.AddUserRequest):
  hashed_password = get_password_hash(add_user_request.password)
  created = datetime.datetime.now(ZoneInfo('Asia/Tokyo'))
  kind_dict = dict(await select_user_kind(db))
  kind_id = kind_dict.get(add_user_request.kind_name)
  new_user = user_schema.UserCreate(username=add_user_request.username, email=add_user_request.email, hashed_password=hashed_password, user_kind_id=kind_id, created=created)
  row = user_model.User(**new_user.dict())
  db.add(row)
  await db.commit()
  await db.refresh(row)
  added_user = user_schema.AddUser(id=row.id, username=add_user_request.username, email=add_user_request.email, created=created, is_active=True, kind_name=add_user_request.kind_name)
  return {"success":True,"error_msg":"","added_user":added_user}

async def add_users(db: AsyncSession, add_user_request: List[user_schema.AddUserRequest]):
  added_users = []
  created = datetime.datetime.now(ZoneInfo('Asia/Tokyo'))
  kind_dict = dict(await select_user_kind(db))
  for add_user in add_user_request:
    hashed_password = get_password_hash(add_user.password)
    kind_id = kind_dict.get(add_user.kind_name)
    new_user = user_schema.UserCreate(username=add_user.username, email=add_user.email, hashed_password=hashed_password, user_kind_id=kind_id, created=created)
    row = user_model.User(**new_user.dict())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    added_user = user_schema.AddUser(id=row.id, username=add_user.username, email=add_user.email, created=created, is_active=True, kind_name=add_user.kind_name)
    added_users.append(added_user)
  return {'success': True, 'error_msg': '', 'added_users': added_users}

async def register_access_history(db: AsyncSession, user: user_schema.User, add_access_history_request: user_schema.AddAccessHistoryRequest):
  access_time = await select_access_history(db=db, user=user, add_access_history_request=add_access_history_request)
  if not access_time:
    await add_access_history(db=db, user=user, add_access_history_request=add_access_history_request)
  else:
    await update_access_history(db=db, user=user, add_access_history_request=add_access_history_request, access_time=access_time['time'])
  await db.commit()
  return {'success': True}

async def get_user_name(db:AsyncSession, user_id: int):
  try:
    result: Result = await(
      db.execute(
        select(
          user_model.User.username
        ).where( user_model.User.id ==  user_id )
      )
    )
    username = result.scalar_one_or_none()
    return username
  except Exception as e:
    print(f"Error fetching username for user_id {user_id}: {e}")
    return None

async def register_login_num(db:AsyncSession, user_id: int):
  today = datetime.date.today()
  result : Result = await(
    db.execute(
      select(
        user_model.Login.login_day
      ).where( user_model.Login.user_id == user_id)
      .where(user_model.Login.login_day == today)
    )
  )
  login_entry = result.scalar_one_or_none()
  if not login_entry:
    new_login = user_model.Login(user_id = user_id, login_day = today)
    point_result : Result = await(
      db.execute(
        update(user_model.User_com)
        .where(user_model.User_com.user_id == user_id)
        .values(point = user_model.User_com.point + 1)
      )
    )
    db.add(new_login)
    await db.flush()
    await db.commit()
    await db.refresh(new_login)
  total_result : Result = await(
    db.execute(
      select(
        user_model.Login.login_day
      ).where(user_model.Login.user_id == user_id)
    )
  )
  login_days = len(total_result.scalars().all())
  if login_days == 10:
    point_result : Result = await(
      db.execute(
        update(user_model.User_com)
        .where(user_model.User_com.user_id == user_id)
        .values(point = user_model.User_com.point + 10)
      )
    )
    await db.flush()
    await db.commit()
  return login_days

async def add_goals_history(db: AsyncSession, user_id: int, add_goals_history_request: user_schema.GoalRequest):
  new_goals_history = user_schema.GoalRequest(details=add_goals_history_request.details)
  row = user_model.Goals(user_id=user_id, details=new_goals_history.details)
  db.add(row)
  point_result : Result = await(
    db.execute(
      update(user_model.User_com)
      .where(user_model.User_com.user_id == user_id)
      .values(point = user_model.User_com.point + 3)
    )
  )
  await db.flush()
  return 'success'

async def register_goals_history(db: AsyncSession, user_id : int, add_goals_history_request: user_schema.GoalRequest):
  await add_goals_history(db=db, user_id=user_id, add_goals_history_request=add_goals_history_request)
  await db.commit()
  return {'success': True}

async def get_goals(db:AsyncSession, user_id : int):
  result : Result = await(
    db.execute(
      select(
        user_model.Goals.goal_id,
        user_model.Goals.details,
        user_model.Goals.completed
      ).where(user_model.Goals.user_id == user_id)
    )
  )
  return result.mappings().all()

async def get_not_goal(db:AsyncSession, user_id : int):
  result : Result = await(
    db.execute(
      select(
        user_model.Goals.goal_id,
        user_model.Goals.details,
        user_model.Goals.completed
      ).where(user_model.Goals.user_id == user_id)
      .where(user_model.Goals.completed == False)
    )
  )
  return result.mappings().all()

async def toggle_completed(db:AsyncSession, user_id : int, toggle_completed_request: user_schema.ToggleRequest ):
  result : Result = await(
    db.execute(
      update(user_model.Goals)
      .where(user_model.Goals.goal_id == toggle_completed_request.goal_id)
      .values(completed = toggle_completed_request.completed)
    )
  )
  await db.flush()
  await db.commit()
  return True

async def up_point(db:AsyncSession, user_id : int, up_point_request: user_schema.PointRequest):
  result : Result = await(
    db.execute(
      update(user_model.User_com)
      .where(user_model.User_com.user_id == user_id)
      .values(point = user_model.User_com.point + up_point_request.point)
    )
  )
  await db.flush()
  await db.commit()
  return True

async def get_point(db:AsyncSession, user_id : int):
  result : Result = await(
    db.execute(
      select(
        user_model.User_com.point
      ).where(user_model.User_com.user_id == user_id)
    )
  )
  return result.scalar_one_or_none()

async def get_high_pointer(db:AsyncSession):
  result : Result = await(
    db.execute(
      select(
        user_model.User_com.user_id,
        user_model.User_com.point
      ).join(user_model.User, user_model.User_com.user_id == user_model.User.id)
      .where(user_model.User.user_kind_id == 3)
      .order_by(desc(user_model.User_com.point))
      .distinct()
      .limit(30)
    )
  )
  members = result.mappings().all()

  higher = []
  for member in members:
    result : Result = await(
      db.execute(
        select(user_model.User.email)
        .where(user_model.User.id == member.user_id)
      ))
    mail_record = result.scalar_one_or_none()

    if mail_record:
      local_part = mail_record.split('@')[0]
      higher.append({
        'mail': local_part,
        'point': member.point
      })
  return higher



async def register_theme(db: AsyncSession, user_id: int, register_theme_request: user_schema.ThemeRequest):
    try:
        data_result = await db.execute(
            select(user_model.User_com).where(user_model.User_com.user_id == user_id)
        )
        data = data_result.mappings().first()

        if data:
            await db.execute(
                update(user_model.User_com)
                .where(user_model.User_com.user_id == user_id)
                .values(theme=register_theme_request.theme)
            )
        else:
            new_user_com = user_model.User_com(user_id=user_id, theme=register_theme_request.theme)
            db.add(new_user_com)

        await db.flush()
        
        try:
            await db.commit()
            return register_theme_request.theme
        except NotSupportedError:
            print("このデータベースはトランザクションをサポートしていません。コミットをスキップします。")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        await db.rollback()
        return False
    finally:
        await db.close()

async def get_theme(db: AsyncSession, user_id: int):
  result : Result = await(
    db.execute(
      select(
        user_model.User_com.theme
      ).where(user_model.User_com.user_id == user_id)
    )
  )
  user_theme = result.scalar()
  return user_theme or 'light'

async def delete_goal(db:AsyncSession, user_id:int, delete_request:user_schema.GoalDeleteRequest):
  result : Result = await(
    db.execute(
      delete(
        user_model.Goals
      ).where(user_model.Goals.user_id == user_id , user_model.Goals.goal_id == delete_request.goal_id)
    )
  )
  await db.commit()
  return {"message": "Goal deleted successfully"}

async def set_nickname(db:AsyncSession, user_id:int, set_nickname_request:user_schema.SetNicknameRequest):
  result : Result = await(
    db.execute(
      update(user_model.User_com)
      .where(user_model.User_com.user_id == user_id)
      .values(nickname = set_nickname_request.nickname)
    )
  )
  await db.flush()
  await db.commit()
  return 'sucsess'

async def get_nickname(db:AsyncSession, user_id:int):
  result : Result = await(
    db.execute(
      select(
        user_model.User_com.nickname
      ).where(user_model.User_com.user_id == user_id)
    )
  )
  return result.scalar_one_or_none()