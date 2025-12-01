from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
import uuid


class Table(Base):
    __tablename__ = "tables"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    table_number = Column(Integer, nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)

    reservations = relationship(
        "Reservation",
        back_populates="table",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Table(id={self.id}, table_number={self.table_number}, capacity={self.capacity})>"
