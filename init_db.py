"""
Скрипт для инициализации базы данных.
Запустите этот скрипт один раз для создания таблиц.
"""

from database import Base, engine

Base.metadata.create_all(bind=engine)
print("База данных инициализирована успешно!")
