# tests/test_reservation_service.py

"""
Тесты для ReservationService (CRUD броней).
"""

import pytest
from datetime import datetime, timedelta

from src.db.crud import TableService, ReservationService
from src.schemas.table import TableCreate
from src.schemas.reservation import ReservationCreate
from src.db.models import Reservation


def test_create_reservation_success(db_session):
    """
    Создание брони без конфликтов.
    """
    table = TableService.create_table(TableCreate(name="Стол для брони", seats=2))

    data = ReservationCreate(
        table_id=table.id,
        reservation_time=datetime.now(),
        duration_minutes=60,
        customer_name="Иван"
    )

    reservation = ReservationService.create_reservation(data)

    assert isinstance(reservation, Reservation)
    assert reservation.customer_name == "Иван"
    assert reservation.table_id == table.id


def test_create_reservation_conflict(db_session):
    """
    Ошибка при создании брони с пересечением.
    """
    table = TableService.create_table(TableCreate(name="Конфликтный", seats=4))
    now = datetime.now()

    ReservationService.create_reservation(ReservationCreate(
        table_id=table.id,
        reservation_time=now,
        duration_minutes=60,
        customer_name="Петр"
    ))

    # Пересекающаяся бронь
    with pytest.raises(Exception) as exc:
        ReservationService.create_reservation(ReservationCreate(
            table_id=table.id,
            reservation_time=now + timedelta(minutes=30),
            duration_minutes=30,
            customer_name="Андрей"
        ))

    assert "забронирован" in str(exc.value)


def test_create_reservation_nonexistent_table(db_session):
    """
    Ошибка при попытке бронировать несуществующий столик.
    """
    with pytest.raises(Exception) as exc:
        ReservationService.create_reservation(ReservationCreate(
            table_id=999,
            reservation_time=datetime.now(),
            duration_minutes=30,
            customer_name="Ошибка"
        ))

    assert "не существует" in str(exc.value)


def test_get_reservations(db_session):
    """
    Получить список всех бронирований.
    """
    table = TableService.create_table(TableCreate(name="Стол от списка", seats=2))
    ReservationService.create_reservation(ReservationCreate(
        table_id=table.id,
        reservation_time=datetime.now(),
        duration_minutes=45,
        customer_name="Ольга"
    ))

    reservations = ReservationService.get_reservations()
    assert len(reservations) >= 1
    assert all(isinstance(res, Reservation) for res in reservations)


def test_delete_reservation_success(db_session):
    """
    Удаление существующей брони.
    """
    table = TableService.create_table(TableCreate(name="Удалить бронь", seats=2))

    reservation = ReservationService.create_reservation(ReservationCreate(
        table_id=table.id,
        reservation_time=datetime.now(),
        duration_minutes=30,
        customer_name="Удаление"
    ))

    deleted = ReservationService.delete_reservation(reservation.id)

    assert deleted.id == reservation.id


def test_delete_reservation_not_found(db_session):
    """
    Удаление несуществующей брони должно выбросить HTTPException.
    """
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc:
        ReservationService.delete_reservation(123456789)

    assert exc.value.status_code == 404
