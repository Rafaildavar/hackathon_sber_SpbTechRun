FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Зависимости root-приложения
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Зависимости AI-сервера (извлекаем из pyproject.toml)
COPY server/pyproject.toml /tmp/server_pyproject.toml
RUN python3 -c "import tomllib; f=open('/tmp/server_pyproject.toml','rb'); d=tomllib.load(f); f.close(); print('\n'.join(d['project']['dependencies']))" > /tmp/server_requirements.txt \
    && pip install --no-cache-dir -r /tmp/server_requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/server/src

EXPOSE 5001

CMD ["python", "app.py"]
