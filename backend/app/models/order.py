from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
import uuid


class Order(Base):
    __tablename__ = "orders"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reservation_id = Column(CHAR(36), ForeignKey(
        "reservations.id"), nullable=False)
    total_price = Column(Integer, default=0)

    reservation = relationship("Reservation", back_populates="order")
    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Order(id={self.id}, reservation_id={self.reservation_id}, total_price={self.total_price})>"
