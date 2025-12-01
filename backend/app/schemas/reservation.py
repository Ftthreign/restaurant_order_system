from pydantic import BaseModel
from datetime import date, time

from app.schemas.customer import CustomerResponse
from app.schemas.table import TableResponse


class ReservationBase(BaseModel):
    customer_id: str
    table_id: str
    date: date
    time: time


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(ReservationBase):
    pass


class ReservationResponse(BaseModel):
    id: str
    customer: CustomerResponse
    table: TableResponse
    date: date
    time: time

    class Config:
        from_attributes = True
