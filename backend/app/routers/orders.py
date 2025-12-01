from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    OrderCreate,
    OrderResponse,
    OrderItemBase,
)
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return OrderService.create_order(db, payload)


@router.post("/{order_id}/items", response_model=OrderResponse)
def add_item(order_id: str, payload: OrderItemBase, db: Session = Depends(get_db)):
    return OrderService.add_order_item(db, order_id, payload)


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return OrderService.get_all_order(db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    return OrderService.get_order(db, order_id)


@router.put("/{order_id}/items/{item_id}", response_model=OrderResponse)
def update_order_item(order_id: str, item_id: str, payload: OrderItemBase, db: Session = Depends(get_db)):
    return OrderService.update_order_item(db, order_id, item_id, payload)


@router.delete("/{order_id}/items/{item_id}", response_model=OrderResponse)
def delete_order_item(order_id: str, item_id: str, db: Session = Depends(get_db)):
    return OrderService.delete_order_item(db, order_id, item_id)
