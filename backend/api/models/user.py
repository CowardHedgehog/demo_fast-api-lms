# ユーザ情報を示すテーブル群
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Date, DATETIME, Float
from sqlalchemy.orm import relationship
import datetime

from api.db import Base

# ユーザ情報
class User(Base):
    __tablename__  = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    #password_last_update = Column(DATETIME, default=datetime.datetime.now(), nullable=False)
    user_kind_id = Column(Integer, ForeignKey('user_kind.id', ondelete="CASCADE"), nullable=False)
    created = Column(DATETIME, default=datetime.datetime.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    user_kind = relationship('UserKind')
  

# 学生のクラス情報
class Student(User):
    __tablename__ = 'students'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    grade = Column(Integer)
    department = Column(String(32))
    classes = Column(Integer)
    number = Column(Integer)
  

# ユーザ種別と作成権限
class UserKind(Base):
    __tablename__ = 'user_kind'
    
    id = Column(Integer, primary_key=True, index=True)
    kind_name = Column(String(128), nullable=False, comment='ユーザの種別名')
    create = Column(Boolean, default=False, nullable=False, comment='コースやフローを作成する権限があるか')


# 推定したユーザの能力値
class IrtAbility(Base):
    __tablename__ = "IRT_Ability"
  
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    flow_id = Column(Integer, ForeignKey('flows.id'), primary_key=True)
    ability = Column(Float, nullable=True)


# アクセス時間
class AccessHistory(Base):
    __tablename__ = 'access_histories'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    date = Column(Date, primary_key=True)
    time = Column(Integer, nullable=True, default=0)
    page = Column(String(128), primary_key=True)
    details = Column(String(512), primary_key=True)

#ログイン日
class Login(Base):
    __tablename__ = 'login'

    user_id = Column(Integer, ForeignKey('users.id'),primary_key = True)
    login_day = Column(Date, primary_key = True)

#設定した目標
class Goals(Base):
    __tablename__ = 'goals'

    goal_id = Column(Integer, primary_key = True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    details = Column(String(128))
    completed = Column(Boolean, default = False)

#ユーザーに関する情報
class User_com(Base):
    __tablename__ = 'user_com'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key = True)
    nickname = Column(String(32))
    theme = Column(String(32))
    point = Column(Integer, default = 0)

#ポイントが入る内容
class Pointlist(Base):
    __tablename__ = "pointlist"

    user_id = Column(Integer,  ForeignKey('users.id'), primary_key = True)
    content = Column(String(64))
    point = Column(Integer)
    flag = Column(Boolean, default = False)
  
