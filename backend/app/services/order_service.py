from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Order, OrderItem, Menu
from app.schemas import OrderCreate, OrderItemBase


class OrderService:

    @staticmethod
    def create_order(db: Session, payload: OrderCreate):
        order = Order(
            reservation_id=payload.reservation_id,
            total_price=0
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def add_order_item(db: Session, order_id: str, item: OrderItemBase):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(404, "Order not found")

        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        if not menu:
            raise HTTPException(404, "Menu not found")

        subtotal = menu.price * item.quantity

        order_item = OrderItem(
            order_id=order.id,
            menu_id=menu.id,
            quantity=item.quantity,
            subtotal=subtotal
        )
        db.add(order_item)

        order.total_price += subtotal

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order(db: Session, order_id: str):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(404, "Order not found")
        return order

    @staticmethod
    def get_all_order(db: Session):
        return db.query(Order).all()

    @staticmethod
    def update_order_item(db: Session, order_id: str, item_id: str, payload: OrderItemBase):
        item = db.query(OrderItem).filter(OrderItem.id == item_id,
                                          OrderItem.order_id == order_id).first()
        if not item:
            raise HTTPException(404, "Order item not found")

        menu = db.query(Menu).filter(Menu.id == payload.menu_id).first()
        if not menu:
            raise HTTPException(404, "Menu not found")

        item.menu_id = payload.menu_id
        item.quantity = payload.quantity
        item.subtotal = menu.price * payload.quantity

        order = item.order
        order.total_price = sum(i.subtotal for i in order.order_items)

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def delete_order_item(db: Session, order_id: str, item_id: str):
        item = db.query(OrderItem).filter(OrderItem.id == item_id,
                                          OrderItem.order_id == order_id).first()
        if not item:
            raise HTTPException(404, "Order item not found")

        order = item.order
        db.delete(item)
        db.commit()

        order.total_price = sum(i.subtotal for i in order.order_items)
        db.commit()
        db.refresh(order)
        return order
