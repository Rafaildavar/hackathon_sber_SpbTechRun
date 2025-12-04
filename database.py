"""
Модели базы данных для приложения.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Создание базового класса для моделей
Base = declarative_base()

# Создание движка базы данных
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5433/city_helper')
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    """Модель пользователя."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    city = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Преобразование объекта в словарь."""
        return {
            'id': self.id,
            'username': self.username,
            'city': self.city,
            'district': self.district,
            'age': self.age,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Chat(Base):
    """Модель чата."""
    __tablename__ = 'chats'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь с пользователем
    user = relationship("User", backref="chats")
    # Связь с сообщениями
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan", order_by="Message.created_at")
    
    def __repr__(self):
        return f'<Chat {self.id}: {self.title}>'
    
    def to_dict(self):
        """Преобразование объекта в словарь."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'message_count': len(self.messages) if self.messages else 0
        }


class Message(Base):
    """Модель сообщения в чате."""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' или 'assistant'
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default='text')  # 'text', 'image', 'audio', 'file'
    message_metadata = Column(JSON, nullable=True)  # Дополнительные данные (имя файла, URL и т.д.)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связь с чатом
    chat = relationship("Chat", back_populates="messages")
    
    def __repr__(self):
        return f'<Message {self.id}: {self.role}>'
    
    def to_dict(self):
        """Преобразование объекта в словарь."""
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'role': self.role,
            'content': self.content,
            'type': self.message_type,
            'metadata': self.message_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# Функция для получения сессии БД
def get_db():
    """Dependency для получения сессии базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
