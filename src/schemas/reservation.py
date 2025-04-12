from pydantic import BaseModel
from datetime import datetime

class ReservationBase(BaseModel):
    customer_name: str
    phone_number: str # для миграции 56be84005fac_add_phone_number_to_reservations
    table_id: int
    reservation_time: datetime
    duration_minutes: int

class ReservationCreate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: int

    model_config = {
        "from_attributes": True
    }
