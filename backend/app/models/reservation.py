from sqlalchemy import Column, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
import uuid


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(CHAR(36), ForeignKey("customers.id"), nullable=False)
    table_id = Column(CHAR(36), ForeignKey("tables.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    customer = relationship("Customer", back_populates="reservations")
    table = relationship("Table", back_populates="reservations")
    order = relationship("Order",
                         back_populates="reservation",
                         uselist=False,
                         cascade="all, delete-orphan"
                         )

    def __repr__(self):
        return (f"<Reservation(id={self.id}, customer_id={self.customer_id}, "
                f"table_id={self.table_id}, date={self.date}, time={self.time})>")
