from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
from app.database import Base
import uuid


class Menu(Base):
    __tablename__ = "menus"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    prica = Column(Integer, nullable=False)

    order_items = relationship("OrderItem", back_populates="menu")

    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}', price={self.prica})>"
