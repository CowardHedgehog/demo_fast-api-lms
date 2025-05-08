from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import io
from os import isatty
from typing import List,Optional
from urllib import response

import api.cruds.user as user_cruds
import api.cruds.image as image_crud

import api.schemas.user as user_schema
import api.schemas.image as image_schema
import api.schemas.flow as flow_schema

from api.db import get_db

router = APIRouter()

@router.get("/get_image/{image_id}", response_model=image_schema.ImageResponse, tags=['image'])
async def get_image(image_id:int, user:user_schema.User=Depends(user_cruds.get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        img_bin = await image_crud.get_image(db=db, image_id=image_id)
        image_stream = io.BytesIO(img_bin.decode('unicode_escape').encode("raw_unicode_escape"))
    return StreamingResponse(content=image_stream, media_type="image/png")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

@router.get("/get_images/{week_id}", response_model=List[image_schema.ImagesResponse], tags=['image'])
async def get_images(week_id:int, user:user_schema.User=Depends(user_cruds.get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        images = await image_crud.get_images(db=db, week_id=week_id)
        return images
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

@router.post("/image", tags=['image'])
async def add_image(AddImage: image_schema.AddImage, user:user_schema.User=Depends(user_cruds.get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        await image_crud.add_image(db=db, AddImage=AddImage)
        return Response(status_code=status.HTTP_201_CREATED)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")


@router.delete("/image/{image_id}", tags=['image'])
async def delete_image(image_id: int, user:user_schema.User=Depends(user_cruds.get_current_active_user), db:AsyncSession=Depends(get_db)):
    if user.is_active:
        await image_crud.delete_image(db=db, image_id=image_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")