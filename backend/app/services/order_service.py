from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Order, OrderItem, Menu
from app.schemas import OrderCreate, OrderItemBase


class OrderService:
    """
    Service class untuk mengelola proses bisnis Order dan OrderItem.
    Mencakup pembuatan order, penambahan item, update item, penghapusan item,
    serta perhitungan ulang total harga.
    """

    @staticmethod
    def create_order(db: Session, payload: OrderCreate):
        """
        Membuat order baru berdasarkan reservasi.

        Parameters:
            db (Session): Session database aktif.
            payload (OrderCreate): Data input berisi reservation_id.

        Returns:
            Order: Objek order yang berhasil dibuat.

        Raises:
            HTTPException: Jika proses penyimpanan gagal.
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
        Menambahkan item menu ke dalam order.

        Parameters:
            db (Session): Session database aktif.
            order_id (str): ID order tujuan.
            item (OrderItemBase): Data menu_id dan quantity.

        Returns:
            Order: Order yang sudah diperbarui dengan item baru.

        Raises:
            HTTPException:
                - 404 jika order tidak ditemukan
                - 404 jika menu tidak ditemukan
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
        Mengambil detail order berdasarkan ID.

        Parameters:
            db (Session): Session database aktif.
            order_id (str): ID order.

        Returns:
            Order: Order yang ditemukan.

        Raises:
            HTTPException: Jika order tidak ditemukan.
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(404, "Order not found")
        return order

    @staticmethod
    def get_all_order(db: Session):
        """
        Mengambil seluruh daftar order.

        Parameters:
            db (Session): Session database aktif.

        Returns:
            list[Order]: Daftar seluruh order.
        """
        return db.query(Order).all()

    @staticmethod
    def update_order_item(db: Session, order_id: str, item_id: str, payload: OrderItemBase):
        """
        Memperbarui item dalam order.

        Parameters:
            db (Session): Session database aktif.
            order_id (str): ID order.
            item_id (str): ID item yang akan diperbarui.
            payload (OrderItemBase): Data menu_id dan quantity baru.

        Returns:
            Order: Order yang sudah diperbarui.

        Raises:
            HTTPException:
                - 404 jika order item tidak ditemukan
                - 404 jika menu tidak ditemukan
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
        Menghapus item dari order dan menghitung ulang total harga.

        Parameters:
            db (Session): Session database aktif.
            order_id (str): ID order.
            item_id (str): ID item yang akan dihapus.

        Returns:
            Order: Order setelah item dihapus dan total diperbarui.

        Raises:
            HTTPException: 404 jika item tidak ditemukan.
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
