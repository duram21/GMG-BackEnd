from sqlalchemy import Column, Integer, String
from database import Base # database.py에서 만든 Base 임포트

class Item(Base):
    __tablename__ = "items" # 실제 데이터베이스 테이블 이름

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)