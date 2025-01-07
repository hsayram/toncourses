import os
from pathlib import Path
from datetime import datetime, timezone

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к базе данных PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = "your_secret_key"

# Инициализация базы данных с помощью SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель пользователя для базы данных
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_premium = Column(Boolean, default=False)
    added_to_attachment_menu = Column(Boolean, default=False)
    allows_write_to_pm = Column(Boolean, default=True)
    photo_url = Column(String, nullable=True)
    
    
# Модели данных
class Course(BaseModel):
    id: int
    title: str
    description: str
    price: float
    is_active: bool

class TelegramUser(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    language_code: str
    is_premium: bool = False
    added_to_attachment_menu: bool = False
    allows_write_to_pm: bool = False
    photo_url: str = None

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()

# Инициализация CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Токен для аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Проверка токена (для защищенных эндпоинтов)
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Основной маршрут для отображения HTML
@app.get("/", response_class=HTMLResponse)
async def root():
    html_file = Path("frontend/index.html")  # Путь к frontend файлу
    if not html_file.exists():
        return {"error": "HTML file not found"}
    return HTMLResponse(content=html_file.read_text(), status_code=200)


# Создание нового пользователя (Telegram-login) и сохранение его в БД
@app.post("/users/telegram-login")
async def telegram_login(user: TelegramUser, db: SessionLocal = Depends(get_db)):
    print(f"Received user data: {user}") 
    # Проверяем, существует ли пользователь в базе данных
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    
    print(db_user)
    print(user)

    if db_user:
        # Если пользователь существует, проверяем, изменились ли его параметры
        user_updated = False

        if db_user.username != user.username:
            db_user.username = user.username
            user_updated = True
        if db_user.first_name != user.first_name:
            db_user.first_name = user.first_name
            user_updated = True
        if db_user.last_name != user.last_name:
            db_user.last_name = user.last_name
            user_updated = True
        if db_user.language_code != user.language_code:
            db_user.language_code = user.language_code
            user_updated = True
        if db_user.is_premium != user.is_premium:
            db_user.is_premium = user.is_premium
            user_updated = True
        if db_user.added_to_attachment_menu != user.added_to_attachment_menu:
            db_user.added_to_attachment_menu = user.added_to_attachment_menu
            user_updated = True
        if db_user.allows_write_to_pm != user.allows_write_to_pm:
            db_user.allows_write_to_pm = user.allows_write_to_pm
            user_updated = True
        if db_user.photo_url != user.photo_url:
            db_user.photo_url = user.photo_url
            user_updated = True

        if user_updated:
            db.commit()  # Коммитим изменения в БД
            db.refresh(db_user)  # Обновляем объект пользователя в Python

        return {"message": "User data updated successfully", "token": jwt.encode({"user_id": user.user_id, "username": user.username}, SECRET_KEY, algorithm="HS256")}
    
    else:
        # Если пользователя нет, создаем нового
        db_user = User(
            user_id=user.user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code,
            created_at=datetime.now(timezone.utc),
            is_premium=user.is_premium,
            added_to_attachment_menu=user.added_to_attachment_menu,
            allows_write_to_pm=user.allows_write_to_pm,
            photo_url=user.photo_url,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Генерация JWT токена
        token = jwt.encode({"user_id": user.user_id, "username": user.username}, SECRET_KEY, algorithm="HS256")
        return {"message": "Login successful", "token": token}