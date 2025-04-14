# tests/test_table_service.py

"""
Тесты для TableService (CRUD столиков).
"""

import pytest
from src.db.crud import TableService
from src.schemas.table import TableCreate
from src.db.models import Table


def test_create_table(db_session):
    """
    Проверяет создание нового столика.
    """
    data = TableCreate(name="Столик 1", seats=4)
    new_table = TableService.create_table(data)

    assert isinstance(new_table, Table)
    assert new_table.name == "Столик 1"
    assert new_table.seats == 4


def test_get_tables(db_session):
    """
    Проверяет, что можно получить список всех столиков.
    """
    # Добавим несколько
    TableService.create_table(TableCreate(name="T1", seats=2))
    TableService.create_table(TableCreate(name="T2", seats=4))

    tables = TableService.get_tables()

    assert len(tables) >= 2
    assert all(isinstance(table, Table) for table in tables)


def test_delete_table_success(db_session):
    """
    Удаление существующего столика.
    """
    table = TableService.create_table(TableCreate(name="Удаляемый", seats=2))
    deleted = TableService.delete_table(table.id)

    assert deleted.id == table.id


def test_delete_table_not_found(db_session):
    """
    Удаление несуществующего столика должно выбросить HTTPException.
    """
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc:
        TableService.delete_table(99999)

    assert exc.value.status_code == 404
