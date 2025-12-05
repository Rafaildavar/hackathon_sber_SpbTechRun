import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from endpoints.api import main_router
from core.services.ServiceManager import service_manager
from utils.logger import get_logger

log = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Запуск приложения: инициализация сервисов...")
    service_manager.initialize()
    log.info("Приложение готово к работе!")
    yield
    log.info("Завершение работы приложения")


app = FastAPI(lifespan=lifespan)

app.default_response_class = JSONResponse

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=6500,
        timeout_keep_alive=300,
        timeout_graceful_shutdown=30
    )