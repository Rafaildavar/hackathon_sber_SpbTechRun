FROM python:3.12-slim

WORKDIR /app/src

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

ENV UV_HTTP_TIMEOUT=300

COPY pyproject.toml /app/

RUN uv pip install --system -r /app/pyproject.toml

COPY src/ /app/src/

RUN ls -la /app/src/config.yml && echo "config.yml скопирован успешно" || echo "ОШИБКА: config.yml не найден!"

RUN mkdir -p /data/chunks /data/bm25

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

EXPOSE 6500

CMD ["python", "main.py"]