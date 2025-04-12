# routers/tables.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.schemas.table import TableCreate, TableRead
from src.db.crud import TableService
from src.db.config_db import get_db

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.get("/", response_model=List[TableRead])
def get_all_tables(db: Session = Depends(get_db)):
    """
    Получить список всех столиков в ресторане.

    - **GET /tables/**
    - Возвращает список всех столов с их параметрами.
    """
    return TableService.get_tables()


@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    """
    Создать новый столик.

    - **POST /tables/**
    - Принимает JSON с параметрами столика.
    - Возвращает созданный объект.
    """
    return TableService.create_table(table)


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    """
    Удалить столик по ID.

    - **DELETE /tables/{id}**
    - Если ID не существует, возвращает 404.
    """
    TableService.delete_table(table_id)
