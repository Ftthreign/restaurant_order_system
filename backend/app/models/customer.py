from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
import uuid


class Customer(Base):
    __tablename__ = "customers"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    phone = Column(String(30), nullable=False, unique=True)

    reservations = relationship(
        "Reservation",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', phone='{self.phone}')>"
