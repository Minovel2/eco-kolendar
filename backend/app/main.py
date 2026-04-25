from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from app import models, schemas, crud
from app.database import engine, get_db
from app.seed import seed_database
import json
from app.models import User
from app.schemas import UserRegister, UserLogin, UserResponse, HolidayUpdate

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Эко-календарь API",
    description="API для экологического и национального календаря праздников",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    seed_database()
    models.Base.metadata.create_all(bind=engine)  # Создаёт все таблицы
    seed_database()

@app.get("/")
async def root():
    return {"message": "Эко-календарь API работает!"}

@app.get("/api/holidays", response_model=List[schemas.HolidayResponse])
async def get_holidays(
    type: Optional[str] = None,
    region: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить список всех праздников с возможностью фильтрации"""
    holidays = crud.filter_holidays(db, type=type, region=region, search=search)
    result = []
    for h in holidays:
        try:
            events = json.loads(h.events) if h.events else []
        except:
            events = []
        result.append({
            "id": h.id,
            "name": h.name,
            "day": h.day,
            "month": h.month,
            "type": h.type,
            "region": h.region,
            "description": h.description,
            "events": events,
            "wikipedia_url": h.wikipedia_url or ""
        })
    return result

@app.post("/api/holidays", response_model=schemas.HolidayResponse)
async def create_holiday(
    holiday: schemas.HolidayCreate,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Добавить новый праздник"""
    # Временно без проверки админа (добавим позже)
    db_holiday = crud.create_holiday(db=db, holiday=holiday)
    try:
        events = json.loads(db_holiday.events) if db_holiday.events else []
    except:
        events = []
    return {
        "id": db_holiday.id,
        "name": db_holiday.name,
        "day": db_holiday.day,
        "month": db_holiday.month,
        "type": db_holiday.type,
        "region": db_holiday.region,
        "description": db_holiday.description,
        "events": events,
        "wikipedia_url": db_holiday.wikipedia_url or ""
    }

@app.get("/api/holidays/{holiday_id}", response_model=schemas.HolidayResponse)
async def get_holiday(
    holiday_id: int,
    db: Session = Depends(get_db)
):
    """Получить праздник по ID"""
    holiday = crud.get_holiday(db, holiday_id=holiday_id)
    if holiday is None:
        raise HTTPException(status_code=404, detail="Праздник не найден")
    try:
        events = json.loads(holiday.events) if holiday.events else []
    except:
        events = []
    return {
        "id": holiday.id,
        "name": holiday.name,
        "day": holiday.day,
        "month": holiday.month,
        "type": holiday.type,
        "region": holiday.region,
        "description": holiday.description,
        "events": events,
        "wikipedia_url": holiday.wikipedia_url or ""
    }

@app.delete("/api/holidays/{holiday_id}")
async def delete_holiday(
    holiday_id: int,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Удалить праздник"""
    # Временно без проверки админа
    success = crud.delete_holiday(db, holiday_id)
    if not success:
        raise HTTPException(status_code=404, detail="Праздник не найден")
    return {"message": "Праздник удалён"}

@app.post("/api/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Регистрация пользователя"""
    user = crud.create_user(db, user_data)
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    return user

@app.post("/api/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Вход в систему"""
    user = crud.login_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "name": f"{user.last_name} {user.first_name}"
    }

@app.put("/api/holidays/{holiday_id}")
async def update_holiday(
    holiday_id: int,
    holiday_data: HolidayUpdate,
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """Обновить праздник"""
    # Временно без проверки админа
    updated = crud.update_holiday(db, holiday_id, holiday_data.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Праздник не найден")
    return {"message": "Праздник обновлён"}