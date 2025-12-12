import asyncio
from typing import Optional, List, Dict
import difflib

# Простая in-memory память и хранилище документов для RAG-мока.
# Документы храним в виде списка словарей с полями: name, text

_MEMORY: Dict[str, List[Dict]] = {}
_DOCS: Dict[str, List[Dict]] = {}


def _get_memory(user_id: str):
    return _MEMORY.setdefault(user_id, [])


def _get_docs(user_id: str):
    return _DOCS.setdefault(user_id, [])


async def handle_user_message(
    user_id: str,
    text: Optional[str] = None,
    document_path: Optional[str] = None,
    document_text: Optional[str] = None,
    document_name: Optional[str] = None,
) -> str:
    """Обрабатывает вход пользователя и возвращает ответ агента (mock RAG).

    Поддерживает передачу текста или документа (как строка). Документы индексируются
    в простое in-memory хранилище; при текстовом запросе возвращаем релевантные
    фрагменты документов (по простому сравнению) и формируем ответ.
    """
    mem = _get_memory(user_id)

    # Если передан путь к локальному файлу — прочитаем его
    if document_path:
        try:
            with open(document_path, "r", encoding="utf-8") as f:
                document_text = f.read()
        except Exception as e:
            return f"Не удалось прочитать документ: {e}"

    # Обработка документа в виде текста
    if document_text is not None:
        docs = _get_docs(user_id)
        name = document_name or "document"
        docs.append({"name": name, "text": document_text})
        mem.append({"role": "user", "type": "document", "name": name, "len": len(document_text)})

        preview = document_text[:1000]
        resp = (
            "[MOCK RAG] Документ принят и сохранён.\n"
            f"Имя: {name}. Длина: {len(document_text)} символов. Превью:\n{preview}\n\n"
            "(Это мок RAG: добавьте реальный движок/векторный стор для полноценных ответов)"
        )
        mem.append({"role": "assistant", "text": resp})
        await asyncio.sleep(0.05)
        return resp

    # Текстовый запрос — выполним простую ретривал-логику по документам
    if text is None:
        return "Пустое сообщение"

    mem.append({"role": "user", "text": text})

    docs = _get_docs(user_id)

    retrieved: List[Dict] = []
    if docs:
        # Оценим схожесть запроса с каждым документом через difflib
        scores = []
        for d in docs:
            # Используем короткий превью документа для сравнения
            sample = d["text"][:2000]
            ratio = difflib.SequenceMatcher(None, text, sample).ratio()
            scores.append((ratio, d))
        scores.sort(key=lambda x: x[0], reverse=True)
        top = [d for _s, d in scores[:3] if _s > 0]
        retrieved = top

    # Формируем ответ — комбинируем простую генерацию с retrieved snippets
    if retrieved:
        parts = [f"[RAG] Нашёл {len(retrieved)} релевантных документа(ов):"]
        for d in retrieved:
            parts.append(f"- {d['name']}: {d['text'][:500].replace('\n', ' ')[:500]}...")
        parts.append("\nОтвет (mock):")
        parts.append(f"[MOCK RAG GENERATION] По вашему запросу: '{text}' — вот краткий ответ (mock).")
        resp = "\n".join(parts)
    else:
        resp = "[MOCK AGENT] " + (f"Echo: {text}" if len(text) < 500 else f"Received {len(text)} chars")

    mem.append({"role": "assistant", "text": resp})
    await asyncio.sleep(0.03)
    return resp


def clear_memory(user_id: str):
    _MEMORY.pop(user_id, None)
    _DOCS.pop(user_id, None)


def get_memory(user_id: str):
    return list(_get_memory(user_id))


def get_documents(user_id: str):
    return list(_get_docs(user_id))
