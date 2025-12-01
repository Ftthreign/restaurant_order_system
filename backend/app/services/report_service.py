from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Order, Reservation, OrderItem, Menu


class ReportService:

    @staticmethod
    def daily_sales(db: Session):
        rows = (
            db.query(
                Reservation.date.label("date"),
                func.sum(Order.total_price).label("total_sales")
            )
            .join(Order, Reservation.id == Order.reservation_id)
            .group_by(Reservation.date)
            .all()
        )

        return [
            {"date": row.date, "total_sales": row.total_sales}
            for row in rows
        ]

    @staticmethod
    def menu_rank(db: Session):
        rows = (
            db.query(
                Menu.name.label("menu"),
                func.sum(OrderItem.quantity).label("qty_sold")
            )
            .join(OrderItem, Menu.id == OrderItem.menu_id)
            .group_by(Menu.id)
            .order_by(func.sum(OrderItem.quantity).desc())
            .all()
        )

        return [
            {"menu": row.menu, "qty_sold": row.qty_sold}
            for row in rows
        ]
