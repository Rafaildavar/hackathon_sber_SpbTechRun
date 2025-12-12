"""
Интеграция мультиагентской системы для бота MAX
"""
import sys
import os
import io
from pathlib import Path
from typing import Optional, List, Dict
import fitz  # PyMuPDF для парсинга PDF

# Добавляем путь к серверу в PYTHONPATH
project_root = Path(__file__).parent.parent
server_path = project_root / "server" / "src"

# Важно: сначала добавить server/src, чтобы импорты config.Config работали
sys.path.insert(0, str(server_path))
sys.path.insert(0, str(project_root))

# Меняем рабочую директорию на server/src для правильных путей
original_cwd = os.getcwd()
os.chdir(server_path)

from core.langgraph_multi_agent.main import UrbanAdvisorSystem, create_initial_state

# Возвращаем рабочую директорию обратно
os.chdir(original_cwd)

# Импорты из корня проекта
from database import SessionLocal, User, Chat, Message
from datetime import datetime


def parse_pdf_from_bytes(pdf_bytes: bytes) -> str:
    """Парсинг PDF из байтов"""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += f"\n--- Страница {page_num + 1} ---\n"
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        return f"Ошибка при парсинге PDF: {str(e)}"


def parse_pdf_from_path(pdf_path: str) -> str:
    """Парсинг PDF из файла"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += f"\n--- Страница {page_num + 1} ---\n"
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        return f"Ошибка при парсинге PDF: {str(e)}"


class MaxBotAgent:
    """Агент для работы с ботом MAX, интегрированный с мультиагентской системой"""

    def __init__(self):
        # Инициализация мультиагентской системы
        self.urban_system = UrbanAdvisorSystem()
        self.graph = self.urban_system.build_graph()

    def get_db(self):
        """Получить сессию БД"""
        return SessionLocal()

    def get_or_create_user(self, max_user_id: str) -> Optional[User]:
        """
        Получить или создать пользователя по MAX user_id.
        MAX user_id используется как username с префиксом max_
        """
        db = self.get_db()
        try:
            username = f"max_{max_user_id}"
            user = db.query(User).filter(User.username == username).first()

            if not user:
                # Создаем нового пользователя для MAX
                # Для MAX пользователей пароль не используется, ставим заглушку
                user = User(
                    username=username,
                    password_hash="$2b$12$MAX_USER_NO_PASSWORD_NEEDED",  # Заглушка для MAX
                    city=None,
                    district=None,
                    age=None
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            return user
        except Exception as e:
            print(f"Ошибка при получении/создании пользователя: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    def get_or_create_active_chat(self, user_id: int) -> Optional[Chat]:
        """Получить активный чат пользователя или создать новый"""
        db = self.get_db()
        try:
            # Ищем последний чат пользователя
            chat = db.query(Chat).filter(
                Chat.user_id == user_id
            ).order_by(Chat.updated_at.desc()).first()

            if not chat:
                # Создаем новый чат
                chat = Chat(
                    user_id=user_id,
                    title="Новый чат",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(chat)
                db.commit()
                db.refresh(chat)

            return chat
        except Exception as e:
            print(f"Ошибка при получении/создании чата: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    def get_chat_history(self, chat_id: int, limit: int = 20) -> List[Dict]:
        """Получить историю чата из БД"""
        db = self.get_db()
        try:
            messages = db.query(Message).filter(
                Message.chat_id == chat_id
            ).order_by(Message.created_at.desc()).limit(limit).all()

            # Преобразуем в формат для мультиагентской системы
            history = []
            for msg in reversed(messages):
                history.append({
                    "role": msg.role,
                    "content": msg.content
                })

            return history
        except Exception as e:
            print(f"Ошибка при получении истории чата: {e}")
            return []
        finally:
            db.close()

    def save_message(self, chat_id: int, role: str, content: str):
        """Сохранить сообщение в БД"""
        db = self.get_db()
        try:
            message = Message(
                chat_id=chat_id,
                role=role,
                content=content,
                message_type="text",
                created_at=datetime.utcnow()
            )
            db.add(message)

            # Обновляем время последнего обновления чата
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                chat.updated_at = datetime.utcnow()

            db.commit()
        except Exception as e:
            print(f"Ошибка при сохранении сообщения: {e}")
            db.rollback()
        finally:
            db.close()

    def create_new_chat(self, user_id: int) -> Optional[Chat]:
        """Создать новый чат для пользователя"""
        db = self.get_db()
        try:
            chat = Chat(
                user_id=user_id,
                title="Новый чат",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(chat)
            db.commit()
            db.refresh(chat)
            return chat
        except Exception as e:
            print(f"Ошибка при создании нового чата: {e}")
            db.rollback()
            return None
        finally:
            db.close()

    async def handle_user_message(
        self,
        max_user_id: str,
        text: Optional[str] = None,
        document_path: Optional[str] = None,
        document_text: Optional[str] = None,
        document_name: Optional[str] = None,
    ) -> str:
        """
        Обработать сообщение пользователя через мультиагентскую систему
        """
        try:
            # Получаем или создаем пользователя
            user = self.get_or_create_user(max_user_id)
            if not user:
                return "Ошибка при создании пользователя. Попробуйте позже."

            # Получаем активный чат
            chat = self.get_or_create_active_chat(user.id)
            if not chat:
                return "Ошибка при создании чата. Попробуйте позже."

            # Получаем историю чата
            history = self.get_chat_history(chat.id)

            # Обработка документов
            if document_path:
                try:
                    with open(document_path, "r", encoding="utf-8") as f:
                        document_text = f.read()
                except Exception as e:
                    return f"Не удалось прочитать документ: {e}"

            if document_text is not None:
                # Сохраняем документ как сообщение пользователя
                doc_info = f"[Прикреплен документ: {document_name or 'document'}]\n\n{document_text}"
                self.save_message(chat.id, "user", doc_info)

                # Автоматически создаем вопрос для анализа документа
                auto_question = "Проанализируй этот документ и расскажи о его содержании."

                # Создаем state с документом
                state = create_initial_state(auto_question, history)
                state['user_documents'] = [{'content': document_text, 'name': document_name or 'document'}]
                state['has_user_documents'] = True

                # Запускаем мультиагентскую систему для анализа
                result = await self.graph.ainvoke(state)

                # Извлекаем ответ
                response = result.get('response')
                if hasattr(response, 'content'):
                    response = response.content
                elif not isinstance(response, str):
                    response = str(response)

                if not response:
                    response = f"Документ '{document_name or 'document'}' получен и проанализирован. Задавайте вопросы по нему!"

                self.save_message(chat.id, "assistant", response)
                return response

            # Обработка обычного текстового сообщения
            if not text:
                return "Пустое сообщение"

            # Сохраняем сообщение пользователя
            self.save_message(chat.id, "user", text)

            # Создаем начальное состояние для мультиагентской системы
            state = create_initial_state(text, history)

            # Запускаем мультиагентскую систему
            result = await self.graph.ainvoke(state)

            # Обработка результатов
            if result.get('is_toxic'):
                response = "Пожалуйста, общайтесь уважительно. Я не могу ответить на токсичные сообщения."
                self.save_message(chat.id, "assistant", response)
                return response

            if result.get('in_clarification_mode'):
                questions = result.get('clarification_questions', [])
                response = "Для ответа на ваш вопрос нужны уточнения:\n\n"
                for i, question in enumerate(questions, 1):
                    response += f"{i}. {question}\n"
                self.save_message(chat.id, "assistant", response)
                return response

            # Получаем ответ от агента
            response = result.get('response')
            if not response:
                response = "Не удалось сгенерировать ответ. Попробуйте переформулировать вопрос."

            # Извлекаем текст из AIMessage, если это объект LangChain
            if hasattr(response, 'content'):
                response = response.content
            elif not isinstance(response, str):
                response = str(response)

            # Сохраняем ответ агента
            self.save_message(chat.id, "assistant", response)

            return response

        except Exception as e:
            error_msg = f"Произошла ошибка при обработке запроса: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return "Извините, произошла ошибка. Попробуйте позже."


# Создаем глобальный экземпляр агента
_agent_instance = None


def get_agent() -> MaxBotAgent:
    """Получить синглтон агента"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = MaxBotAgent()
    return _agent_instance


# Функция для обратной совместимости с существующим кодом
async def handle_user_message(
    user_id: str,
    text: Optional[str] = None,
    document_path: Optional[str] = None,
    document_text: Optional[str] = None,
    document_name: Optional[str] = None,
) -> str:
    """Обработка сообщения пользователя"""
    agent = get_agent()
    return await agent.handle_user_message(
        user_id, text, document_path, document_text, document_name
    )


def clear_memory(user_id: str):
    """Очистить контекст пользователя (создать новый чат)"""
    agent = get_agent()
    user = agent.get_or_create_user(user_id)
    if user:
        chat = agent.create_new_chat(user.id)
        if chat:
            return True
    return False


def get_memory(user_id: str):
    """Получить историю чата пользователя"""
    agent = get_agent()
    user = agent.get_or_create_user(user_id)
    if user:
        chat = agent.get_or_create_active_chat(user.id)
        if chat:
            return agent.get_chat_history(chat.id)
    return []


def get_documents(user_id: str):
    """Заглушка для совместимости"""
    return []