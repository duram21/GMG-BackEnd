from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager # 1. 임포트 추가

# .py 파일들이 같은 폴더에 있으므로 '.' 없이 임포트
import models
import schemas
import database
from database import SessionLocal, engine # engine은 여기서도 필요

# 2. ⬇️⬇️⬇️ 이 줄을 여기서 삭제합니다! ⬇️⬇️⬇️
# models.Base.metadata.create_all(bind=engine) 


# 3. ⬇️⬇️⬇️ "lifespan" 이벤트 핸들러 추가 ⬇️⬇️⬇️
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 앱이 시작될 때 ---
    print("INFO:     Application startup... trying to create DB tables.")
    try:
        # DB 테이블 생성 시도
        models.Base.metadata.create_all(bind=engine)
        print("INFO:     DB tables created successfully.")
    except Exception as e:
        print(f"ERROR:    Could not create DB tables: {e}")
    
    yield
    # --- 앱이 종료될 때 ---
    print("INFO:     Application shutdown.")


# 4. FastAPI 앱 생성 시 lifespan 적용
app = FastAPI(lifespan=lifespan)

# 5. CORS 미들웨어 설정 (기존 코드)
origins = [
    "http://localhost:3000",  # React 개발 서버 주소
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. DB 세션 Dependency (기존 코드)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- 7. API 엔드포인트 (기존 코드) ---

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item