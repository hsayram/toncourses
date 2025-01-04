from pathlib import Path
from typing import List

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

SECRET_KEY = "your_secret_key"

# Токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Добавление CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (для тестирования, можно настроить конкретные домены)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Функция проверки токена
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Модель курса
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

# "База данных" в памяти
courses_db: List[Course] = [
    Course(id=1, title="Python Basics", description="Learn the basics of Python.", price=29.99, is_active=True),
    Course(id=2, title="FastAPI Guide", description="Master FastAPI for backend development.", price=39.99, is_active=True),
]

@app.get("/", response_class=HTMLResponse)
async def root():
    html_file = Path("index.html")  # Убедитесь, что путь правильный
    if not html_file.exists():
        return {"error": "HTML file not found"}
    return HTMLResponse(content=html_file.read_text(), status_code=200)

# Получить список всех курсов (защищённый эндпоинт)
@app.get("/courses", response_model=List[Course])
async def get_courses(user: dict = Depends(verify_token)):
    return courses_db

# Получить курс по ID (защищённый эндпоинт)
@app.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: int, user: dict = Depends(verify_token)):
    for course in courses_db:
        if course.id == course_id:
            return course
    return {"error": "Course not found"}

# Создать новый курс (защищённый эндпоинт)
@app.post("/courses", response_model=Course)
async def create_course(course: Course, user: dict = Depends(verify_token)):
    courses_db.append(course)
    return course

@app.put("/courses/{course_id}", response_model=Course)
async def update_course(course_id: int, updated_course: Course, user: dict = Depends(verify_token)):
    for index, course in enumerate(courses_db):
        if course.id == course_id:
            courses_db[index] = updated_course
            return updated_course
    raise HTTPException(status_code=404, detail="Course not found")

@app.delete("/courses/{course_id}", status_code=204)
async def delete_course(course_id: int, user: dict = Depends(verify_token)):
    for index, course in enumerate(courses_db):
        if course.id == course_id:
            courses_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Course not found")

@app.get("/courses/search")
async def search_courses(query: str, user: dict = Depends(verify_token)):
    results = [course for course in courses_db if query.lower() in course.title.lower()]
    return results

@app.get("/courses/filter")
async def filter_courses(is_active: bool, user: dict = Depends(verify_token)):
    filtered_courses = [course for course in courses_db if course.is_active == is_active]
    return filtered_courses


@app.post("/users/telegram-login")
async def telegram_login(user: TelegramUser):
    print(f"Received user data: {user}")  # Логирование данных пользователя
    token = jwt.encode({"user_id": user.user_id, "username": user.username}, SECRET_KEY, algorithm="HS256")
    return {"message": "Login successful", "token": token}