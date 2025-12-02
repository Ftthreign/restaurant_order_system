from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Order, Reservation, OrderItem, Menu


class ReportService:
    """
    Service class for generating analytical reports.
    Provides methods for summarizing daily sales and ranking menu popularity.
    """

    @staticmethod
    def daily_sales(db: Session):
        """
        Generate daily sales summary.

        Retrieves total sales grouped by reservation date. Each row represents
        the sum of all order totals for a specific day.

        Parameters:
            db (Session): Active database session.

        Returns:
            list[dict]: List of dictionaries containing:
                - date: Reservation date
                - total_sales: Total income for that date
        """
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
        """
        Generate ranking of menu items by total quantity sold.

        Calculates total quantity sold per menu item across all orders and
        sorts them in descending order of popularity.

        Parameters:
            db (Session): Active database session.

        Returns:
            list[dict]: List of dictionaries containing:
                - menu: Menu item name
                - qty_sold: Total quantity sold
        """
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
