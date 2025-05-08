from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy import true
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from api.db import get_db
from api.schemas.token import Token, FormData, LogoutResponse
from api.cruds.user import authenticate_user
from api.cruds.domains.generate_token import create_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

@router.post('/token', response_model=Token, tags=['auth'])
async def login_for_access_token(form_data: FormData, db: AsyncSession = Depends(get_db)):
  user = await authenticate_user(db, form_data.email, form_data.password)
  if not user:
    raise HTTPException(
      status_code = status.HTTP_401_UNAUTHORIZED,
      detail = 'Incorrect username or password',
      headers = {'WWW-Authenticate': 'Bearer'}
    )
  access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = await create_access_token(data = {'sub': user.email}, expires_delta = access_token_expires)
  content = {'access_token': access_token, 'token_type': 'bearer'}
  response = JSONResponse(content = content)
  response.set_cookie(key = 'token', value = access_token, httponly = True)
  return response

@router.post('/logout', response_model=LogoutResponse, tags=['auth'])
async def logout():
  response = JSONResponse(content = {})
  response.set_cookie(key = 'token', value = "", expires = 0, httponly = True)
  return response