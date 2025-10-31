from pydantic import BaseModel

# --- Item ---

# API를 통해 받을 데이터 (생성용)
class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

# API를 통해 보낼 데이터 (조회용)
class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True # SQLAlchemy 모델을 Pydantic 모델로 변환