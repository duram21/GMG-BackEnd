import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# docker-compose.yml에서 설정한 환경 변수(DATABASE_URL)를 읽어옴
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

# SQLAlchemy 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# DB 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 모델을 만들기 위한 기본 Base 클래스
Base = declarative_base()