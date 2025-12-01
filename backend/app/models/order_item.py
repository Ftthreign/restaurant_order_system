from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
import uuid


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(CHAR(36), ForeignKey('orders.id'), nullable=False)
    menu_id = Column(CHAR(36), ForeignKey('menus.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    menu = relationship("Menu", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, menu_id={self.menu_id}, quantity={self.quantity}, subtotal={self.subtotal})>"
