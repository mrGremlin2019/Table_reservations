"""
Точка входа в приложение FastAPI
"""

from fastapi import FastAPI
from src.routers import tables, reservations
from src.db.config_db import engine
from src.db.models import Base
import logging

app = FastAPI(title="Restaurant Booking API",
              description="Сервис для бронирования столов в заведении")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

def init_db():
    """Инициализация таблиц БД"""
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    """Запуск приложения"""
    init_db()
    app.include_router(tables.router)
    app.include_router(reservations.router)
    logger.info("Application started")



