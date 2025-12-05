"""
Основной файл FastAPI приложения для городского помощника.
"""

from fastapi import FastAPI, Request, Response, Depends, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Optional
from contextlib import asynccontextmanager
import os
from datetime import datetime
from database import Base, engine, get_db, User, Chat, Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создание таблиц при запуске приложения."""
    try:
        Base.metadata.create_all(bind=engine)
        print("База данных подключена и таблицы созданы/проверены")
    except Exception as e:
        print(f"Предупреждение: не удалось подключиться к базе данных: {e}")
        print("Приложение запустится, но функции БД могут не работать")
    yield
    # Здесь можно добавить код для закрытия соединений при остановке


app = FastAPI(
    title="Городской помощник",
    description="AI-помощник для жителей Санкт-Петербурга",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка статических файлов и шаблонов
app.mount("/resources/static", StaticFiles(directory="resources/static"), name="static")
templates = Jinja2Templates(directory="resources/templates")

# Настройка для работы с паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
SESSION_COOKIE_NAME = 'session_id'


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширование пароля."""
    return pwd_context.hash(password)


def get_current_user(
    session_id: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Получение текущего пользователя из сессии."""
    if not session_id:
        return None
    
    try:
        user_id = int(session_id)
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except (ValueError, TypeError):
        return None


def login_required(current_user: Optional[User] = Depends(get_current_user)):
    """Dependency для проверки авторизации."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    return current_user


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/api/register')
async def register(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя."""
    data = await request.json()
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    city = data.get('city', '').strip()
    district = data.get('district', '').strip()
    age = data.get('age', '').strip()
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Логин и пароль обязательны'
        )
    
    if len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пароль должен содержать минимум 6 символов'
        )
    
    # Проверка существования пользователя
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким логином уже существует'
        )
    
    # Создание нового пользователя
    try:
        user = User(
            username=username,
            password_hash=get_password_hash(password),
            city=city if city else None,
            district=district if district else None,
            age=int(age) if age and age.isdigit() else None
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Установка cookie для автоматического входа
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=str(user.id),
            httponly=True,
            samesite='lax'
        )
        
        return {
            'message': 'Регистрация успешна',
            'user': {
                'id': user.id,
                'username': user.username,
                'city': user.city,
                'district': user.district,
                'age': user.age
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при регистрации: {str(e)}'
        )


@app.post('/api/login')
async def login(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Вход пользователя."""
    data = await request.json()
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Логин и пароль обязательны'
        )
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль'
        )
    
    # Установка cookie
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=str(user.id),
        httponly=True,
        samesite='lax'
    )
    
    return {
        'message': 'Вход выполнен успешно',
        'user': {
            'id': user.id,
            'username': user.username,
            'city': user.city,
            'district': user.district,
            'age': user.age
        }
    }


@app.post('/api/logout')
async def logout(
    response: Response,
    current_user: User = Depends(login_required)
):
    """Выход пользователя."""
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return {'message': 'Выход выполнен успешно'}


@app.get('/api/user')
async def get_user(current_user: User = Depends(login_required)):
    """Получение данных текущего пользователя."""
    return {
        'id': current_user.id,
        'username': current_user.username,
        'city': current_user.city,
        'district': current_user.district,
        'age': current_user.age,
        'created_at': current_user.created_at.isoformat() if current_user.created_at else None
    }


@app.put('/api/user')
async def update_user(
    request: Request,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Обновление данных пользователя."""
    data = await request.json()
    
    if 'city' in data:
        current_user.city = data['city'].strip() if data['city'] else None
    if 'district' in data:
        current_user.district = data['district'].strip() if data['district'] else None
    if 'age' in data:
        age = data['age']
        current_user.age = int(age) if age and str(age).isdigit() else None
    
    try:
        current_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(current_user)
        return {
            'message': 'Данные обновлены успешно',
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'city': current_user.city,
                'district': current_user.district,
                'age': current_user.age
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при обновлении: {str(e)}'
        )


@app.post('/api/change-password')
async def change_password(
    request: Request,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Изменение пароля пользователя."""
    data = await request.json()
    current_password = data.get('currentPassword', '').strip()
    new_password = data.get('newPassword', '').strip()
    confirm_password = data.get('confirmPassword', '').strip()
    
    if not current_password or not new_password or not confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Все поля обязательны'
        )
    
    if not verify_password(current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Текущий пароль неверен'
        )
    
    if new_password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Новые пароли не совпадают'
        )
    
    if len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пароль должен содержать минимум 6 символов'
        )
    
    try:
        current_user.password_hash = get_password_hash(new_password)
        current_user.updated_at = datetime.utcnow()
        db.commit()
        return {'message': 'Пароль успешно изменен'}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при изменении пароля: {str(e)}'
        )


@app.get('/api/check-auth')
async def check_auth(current_user: Optional[User] = Depends(get_current_user)):
    """Проверка авторизации пользователя."""
    if current_user:
        return {
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'city': current_user.city,
                'district': current_user.district,
                'age': current_user.age
            }
        }
    return {'authenticated': False}


# Роуты для страниц
@app.get('/auth/login', response_class=HTMLResponse)
async def login_page(request: Request):
    """Страница входа."""
    return templates.TemplateResponse("auth/auth.html", {"request": request})


@app.get('/auth/register', response_class=HTMLResponse)
async def register_page(request: Request):
    """Страница регистрации."""
    return templates.TemplateResponse("auth/regist.html", {"request": request})


@app.get('/profile', response_class=HTMLResponse)
async def profile_page(request: Request):
    """Страница профиля."""
    return templates.TemplateResponse("profile/profile.html", {"request": request})


@app.get('/api/chats')
async def get_chats(
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Получение списка чатов пользователя."""
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).order_by(Chat.updated_at.desc()).all()
    return [chat.to_dict() for chat in chats]


@app.post('/api/chats')
async def create_chat(
    request: Request,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Создание нового чата."""
    data = await request.json()
    title = data.get('title', 'New Chat').strip()
    
    if not title:
        title = 'New Chat'
    
    try:
        chat = Chat(
            user_id=current_user.id,
            title=title
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat.to_dict()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при создании чата: {str(e)}'
        )


@app.get('/api/chats/{chat_id}')
async def get_chat(
    chat_id: int,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Получение чата по ID."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Чат не найден'
        )
    return chat.to_dict()


@app.put('/api/chats/{chat_id}')
async def update_chat(
    chat_id: int,
    request: Request,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Обновление чата (например, изменение названия)."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Чат не найден'
        )
    
    data = await request.json()
    if 'title' in data:
        chat.title = data['title'].strip() if data['title'] else 'New Chat'
    
    try:
        chat.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(chat)
        return chat.to_dict()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при обновлении чата: {str(e)}'
        )


@app.delete('/api/chats/{chat_id}')
async def delete_chat(
    chat_id: int,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Удаление чата."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Чат не найден'
        )
    
    try:
        db.delete(chat)
        db.commit()
        return {'message': 'Чат успешно удален'}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при удалении чата: {str(e)}'
        )


@app.get('/api/chats/{chat_id}/messages')
async def get_messages(
    chat_id: int,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Получение сообщений чата."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Чат не найден'
        )
    
    messages = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at.asc()).all()
    return [msg.to_dict() for msg in messages]


@app.post('/api/chats/{chat_id}/messages')
async def create_message(
    chat_id: int,
    request: Request,
    current_user: User = Depends(login_required),
    db: Session = Depends(get_db)
):
    """Создание сообщения в чате."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Чат не найден'
        )
    
    data = await request.json()
    role = data.get('role', 'user')  # 'user' или 'assistant'
    content = data.get('content', '').strip()
    message_type = data.get('type', 'text')
    metadata = data.get('metadata', None)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Содержимое сообщения не может быть пустым'
        )
    
    if role not in ['user', 'assistant']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Роль должна быть "user" или "assistant"'
        )
    
    try:
        message = Message(
            chat_id=chat_id,
            role=role,
            content=content,
            message_type=message_type,
            message_metadata=metadata
        )
        db.add(message)
        # Обновляем время последнего обновления чата
        chat.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(message)
        return message.to_dict()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при создании сообщения: {str(e)}'
        )


@app.get('/chat', response_class=HTMLResponse)
async def chat_page(request: Request):
    """Страница чата."""
    return templates.TemplateResponse("chat/chat.html", {"request": request})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5001, reload=True)
