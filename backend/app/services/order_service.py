from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Order, OrderItem, Menu
from app.schemas import OrderCreate, OrderItemBase


class OrderService:
    """
    Service class for handling business logic of Orders and OrderItems.
    Includes creating orders, adding items, updating items, deleting items,
    and recalculating the total price.
    """

    @staticmethod
    def create_order(db: Session, payload: OrderCreate):
        """
        Create a new order based on reservation.

        Parameters:
            db (Session): Active database session.
            payload (OrderCreate): Input containing reservation_id.

        Returns:
            Order: Newly created order instance.

        Raises:
            HTTPException: If saving fails.
        """
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
        """
        Add a menu item into an order.

        Parameters:
            db (Session): Active database session.
            order_id (str): Target order ID.
            item (OrderItemBase): Contains menu_id and quantity.

        Returns:
            Order: Updated order with the added item.

        Raises:
            HTTPException:
                - 404 if order not found
                - 404 if menu not found
        """
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
        """
        Retrieve an order by ID.

        Parameters:
            db (Session): Active database session.
            order_id (str): Order ID.

        Returns:
            Order: Found order.

        Raises:
            HTTPException: If order not found.
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(404, "Order not found")
        return order

    @staticmethod
    def get_all_order(db: Session):
        """
        Retrieve all orders.

        Parameters:
            db (Session): Active database session.

        Returns:
            list[Order]: List of orders.
        """
        return db.query(Order).all()

    @staticmethod
    def update_order_item(db: Session, order_id: str, item_id: str, payload: OrderItemBase):
        """
        Update an existing item inside an order.

        Parameters:
            db (Session): Active database session.
            order_id (str): Order ID.
            item_id (str): Item ID to update.
            payload (OrderItemBase): Contains new menu_id and quantity.

        Returns:
            Order: Updated order.

        Raises:
            HTTPException:
                - 404 if order item not found
                - 404 if menu not found
        """
        item = db.query(OrderItem).filter(
            OrderItem.id == item_id,
            OrderItem.order_id == order_id
        ).first()

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
        """
        Delete an item from an order and recalculate total price.

        Parameters:
            db (Session): Active database session.
            order_id (str): Order ID.
            item_id (str): Item ID to delete.

        Returns:
            Order: Updated order after deletion.

        Raises:
            HTTPException: 404 if item not found.
        """
        item = db.query(OrderItem).filter(
            OrderItem.id == item_id,
            OrderItem.order_id == order_id
        ).first()

        if not item:
            raise HTTPException(404, "Order item not found")

        order = item.order
        db.delete(item)
        db.commit()

        order.total_price = sum(i.subtotal for i in order.order_items)
        db.commit()
        db.refresh(order)
        return order
