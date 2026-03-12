FROM python:3.12-slim

WORKDIR /app/src

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Зависимости (извлекаем из pyproject.toml)
COPY pyproject.toml /app/
RUN python3 -c "import tomllib; f=open('/app/pyproject.toml','rb'); d=tomllib.load(f); f.close(); print('\n'.join(d['project']['dependencies']))" > /tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY src/ /app/src/

RUN ls -la /app/src/config.yml && echo "config.yml OK" || echo "ОШИБКА: config.yml не найден!"

RUN mkdir -p /data/chunks /data/bm25

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

EXPOSE 6500

CMD ["python", "main.py"]
