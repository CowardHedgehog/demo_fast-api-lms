from pydantic import BaseModel


class ImageResponse(BaseModel):
    image_data: bytes

class ImageCreate(BaseModel):
    name: str
    week_id: int
    imgdata: bytes

class ImagesResponse(BaseModel):
    id: int
    name: str
    
class AddImage(BaseModel):
    name: str
    week_id: int
    imgdata: str