import  api.schemas.user as user_schema
from fastapi import  Depends,HTTPException,status
import re
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, delete

import api.models.image as image_model

import api.schemas.image as image_schema



async def select_image(db:AsyncSession, image_id: int) -> image_schema.ImageResponse:
    result: Result = await(
        db.execute(
            select(
                image_model.Image.imgdata,
            ).where(image_model.Image.id == image_id)
        )
    )
    return result.first()

async def select_images(db:AsyncSession, week_id: int) -> image_schema.ImageResponse:
    result: Result = await(
        db.execute(
            select(
                image_model.Image.id,
                image_model.Image.name,
            ).where(image_model.Image.week_id == week_id)
            .order_by(image_model.Image.name)
        )
    )
    return result.mappings().all()

async def get_image(db:AsyncSession, image_id:int):
    image_response = await select_image(db=db, image_id=image_id)
    image_only = image_response[0]
    return image_only

async def get_images(db:AsyncSession, week_id:int):
    images_response = await select_images(db=db, week_id=week_id)
    return images_response

async def add_image(db: AsyncSession, AddImage: image_schema.AddImage):
    image_data = AddImage.imgdata.encode()
    print(image_data)
    
    new_image = image_schema.ImageCreate(name=AddImage.name, week_id=AddImage.week_id, imgdata=image_data)
    print(f"Type of imgdata before insert: {type(new_image.imgdata)}")
    row = image_model.Image(**new_image.dict())
    db.add(row)
    await db.flush()
    await db.commit()
    
async def delete_image(db: AsyncSession, image_id: int):
    result: Result = await(
        db.execute(
            delete(image_model.Image)
            .where(image_model.Image.id == image_id)
        )
    )
    await db.commit()
    return "success"





def replace_images_with_options(content: str, image_map: dict) -> str:
    """
    コンテンツ内の画像URLを置換する関数。

    画像URLは、`[image/画像名]`の形式で指定されていると仮定しています。
    widthやheightのオプション指定が可能
    [image/img1.png] -> <img src='http://localhost:8000/get_image/1' />
    [image/img2.png width=400] -> <img src='http://localhost:8000/get_image/2' width='400' />
    [image/img3.png height=300] -> <img src='http://localhost:8000/get_image/3' height='300' />
    [image/img4.png width=400 height=300] -> <img src='http://localhost:8000/get_image/4' width='400' height='300' />

    Args:
        content (str): 置換対象のコンテンツ
        image_map (dict): 画像IDと画像名のマッピング辞書
                例: {'img1.png': 1, 'img2.png': 2, ...}
        
    Returns:
        content (str): 置換後のコンテンツ
    """
    pattern = r"\[\s*image/([^\s\]]+)(.*?)\s*\]"

    def repl(match):
        image_name = match.group(1)
        options_str = match.group(2)

        image_id = image_map.get(image_name)
        if image_id is None:
            return match.group(0)

        options = dict(re.findall(r'(\w+)=([^\s]+)', options_str))
        width = options.get('width')
        height = options.get('height')

        width_attr = f" width='{width}'" if width else ""
        height_attr = f" height='{height}'" if height else ""

        return f"<img src='http://localhost:8000/get_image/{image_id}'{width_attr}{height_attr} />"

    return re.sub(pattern, repl, content)
    
