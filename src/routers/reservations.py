# routers/reservations.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.schemas.reservation import ReservationCreate, ReservationRead
from src.db.crud import ReservationService
from src.db.config_db import get_db

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/", response_model=List[ReservationRead])
def get_all_reservations(db: Session = Depends(get_db)):
    """
    Получить список всех броней.

    - **GET /reservations/**
    - Возвращает список всех активных броней.
    """
    return ReservationService.get_reservations()


@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    """
    Создать новую бронь.

    - **POST /reservations/**
    - Принимает JSON с параметрами брони.
    - Проверяет, свободен ли столик в это время.
    - Если нет — 400 с сообщением об ошибке.
    - Возвращает созданную бронь.
    """
    return ReservationService.create_reservation(reservation)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Удалить бронь по ID.

    - **DELETE /reservations/{id}**
    - Если ID не существует — 404.
    """
    ReservationService.delete_reservation(reservation_id)
