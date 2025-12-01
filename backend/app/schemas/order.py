from pydantic import BaseModel
from typing import List, Optional
from app.schemas import MenuResponse


class OrderItemBase(BaseModel):
    menu_id: str
    quantity: int


class OrderItemResponse(BaseModel):
    id: str
    quantity: int
    subtotal: int
    menu: MenuResponse

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    reservation_id: str
    total_price: Optional[int] = 0


class OrderCreate(OrderBase):
    pass


class OrderResponse(BaseModel):
    id: str
    reservation_id: str
    total_price: int
    order_items: List[OrderItemResponse]

    class Config:
        from_attributes = True
