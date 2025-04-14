# tests/conftest.py

"""
conftest.py — настройка окружения и тестов для PostgreSQL.

- Загружается конфигурация из .test.env
- Инициализируется тестовая база данных PostgreSQL
- Переопределяется get_db
- Создаётся TestClient
"""

import pytest
from src.db.models import Base
from src.db.config_db import settings, engine
from src.db.config_db import get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
       Создание всех таблиц в тестовой БД перед запуском тестов.
    """
    assert settings.MODE == "TEST"
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(setup_database):
    """Подключение к БД"""
    with get_db() as session:
        yield session
