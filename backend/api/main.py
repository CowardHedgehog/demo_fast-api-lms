from fastapi import FastAPI
from api.routers import auth, user, course, week, flow, image, subject, announcement
from starlette.middleware.cors import CORSMiddleware
import os

tags_metadata = [
  {
    'name': 'users',
  },{
    'name': 'auth',
  },{
    'name': 'create_course'
  },{
    'name': 'flow'
  },{
    'name': 'course'
  },{
    'name': 'week'
  },{
    'name': 'image'
  },{
    'name': 'subject'
  },{
    'name': 'announcement',
    'description': 'お知らせ管理機能'
  }
]

app = FastAPI()


VERCEL_PREVIEW_BACKEND_ORIGIN_REGEX = r"^https://demo-fast-api-lms-[a-zA-Z0-9]+\.vercel\.app$"
VERCEL_PREVIEW_FRONTEND_ORIGIN_REGEX = r"^https://demo-fast-api-lmsfrontend-[a-zA-Z0-9]+\.vercel\.app$"

origins = [
  VERCEL_PREVIEW_FRONTEND_ORIGIN_REGEX,
  VERCEL_PREVIEW_BACKEND_ORIGIN_REGEX,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins_regex=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(course.router)
app.include_router(week.router)
app.include_router(flow.router)
app.include_router(image.router)
app.include_router(subject.router)
app.include_router(announcement.router)
