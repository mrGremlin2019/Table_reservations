from datetime import timedelta
import logging

from sqlalchemy import func, cast
from sqlalchemy.types import Interval

from fastapi import HTTPException
from src.schemas.table import TableCreate
from src.schemas.reservation import ReservationCreate
from src.db.models import Table, Reservation
from src.db.config_db import get_db

logger = logging.getLogger(__name__)


class TableService:
    """
    Сервис для управления столиками в ресторане:
    - получение списка столиков
    - создание
    - удаление
    """

    @staticmethod
    def get_tables():
        """
        Получить список всех столиков (отсортировано по ID).
        """
        with get_db() as db:
            return db.query(Table).order_by(Table.id).all()

    @staticmethod
    def create_table(table_data: TableCreate):
        """
        Создать новый столик.

        :param table_data: данные нового столика
        :return: созданный объект Table
        """
        with get_db() as db:
            new_table = Table(**table_data.model_dump())
            db.add(new_table)
            db.commit()
            db.refresh(new_table)
            logger.info(f"Создан новый столик: {new_table.name} (ID: {new_table.id})")
            return new_table

    @staticmethod
    def delete_table(table_id: int):
        """
        Удалить столик по ID.

        :param table_id: идентификатор столика
        :raises HTTPException: если столик не найден
        :return: удалённый объект Table
        """
        with get_db() as db:
            table = db.query(Table).filter_by(id=table_id).first()
            if not table:
                logger.warning(f"Попытка удалить несуществующий столик (ID: {table_id})")
                raise HTTPException(status_code=404, detail="Столик не найден")
            db.delete(table)
            db.commit()
            logger.info(f"Удалён столик (ID: {table_id})")
            return table


class ReservationService:
    """
    Сервис для управления бронями:
    - создание (с проверкой конфликтов)
    - удаление
    - получение всех броней
    """

    @staticmethod
    def get_reservations():
        """
        Получить список всех броней (отсортировано по времени).
        """
        with get_db() as db:
            return db.query(Reservation).order_by(Reservation.reservation_time).all()

    @staticmethod
    def create_reservation(reservation_data: ReservationCreate):
        """
        Создать новую бронь. Проверяет:
        - Существование указанного столика
        - Конфликт по времени (пересечение)

        :param reservation_data: данные новой брони
        :raises HTTPException: если есть конфликт или столик не найден
        :return: созданный объект Reservation
        """
        with get_db() as db:
            start_time = reservation_data.reservation_time
            end_time = start_time + timedelta(minutes=reservation_data.duration_minutes)

            # Проверка существования столика
            table = db.query(Table).filter_by(id=reservation_data.table_id).first()
            if not table:
                logger.warning(
                    f"Пользователь пытается забронировать несуществующий столик (ID: {reservation_data.table_id})")
                raise HTTPException(status_code=404, detail="Указанный столик не существует")

            # Проверка на пересечение по времени
            overlapping = db.query(Reservation).filter(
                Reservation.table_id == reservation_data.table_id,
                Reservation.reservation_time < end_time,
                (Reservation.reservation_time + cast(func.concat(Reservation.duration_minutes, ' minutes'),
                                                     Interval)) > start_time
            ).first()

            if overlapping:
                logger.info(
                    f"Конфликт брони: столик ID {reservation_data.table_id} уже забронирован с "
                    f"{overlapping.reservation_time} на {overlapping.duration_minutes} минут"
                )
                raise HTTPException(
                    status_code=400,
                    detail="Этот столик уже забронирован на указанное время"
                )

            # Если всё ок — создаём
            new_reservation = Reservation(**reservation_data.model_dump())
            db.add(new_reservation)
            db.commit()
            db.refresh(new_reservation)
            logger.info(
                f"Создана новая бронь: столик {new_reservation.table_id}, клиент {new_reservation.customer_name}, "
                f"время {new_reservation.reservation_time}, длительность {new_reservation.duration_minutes} мин"
            )
            return new_reservation

    @staticmethod
    def delete_reservation(reservation_id: int):
        """
        Удалить бронь по ID.

        :param reservation_id: идентификатор брони
        :raises HTTPException: если бронь не найдена
        :return: удалённый объект Reservation
        """
        with get_db() as db:
            reservation = db.query(Reservation).filter_by(id=reservation_id).first()
            if not reservation:
                logger.warning(f"Попытка удалить несуществующую бронь (ID: {reservation_id})")
                raise HTTPException(status_code=404, detail="Бронь не найдена")
            db.delete(reservation)
            db.commit()
            logger.info(f"Удалена бронь (ID: {reservation_id})")
            return reservation
