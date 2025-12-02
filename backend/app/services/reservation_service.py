from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Reservation
from app.schemas import ReservationCreate, ReservationUpdate


class ReservationService:
    """
    Service class for managing Reservation CRUD operations.
    Handles creation, retrieval, update, and deletion of reservation records.
    """

    @staticmethod
    def create_reservation(db: Session, payload: ReservationCreate):
        """
        Create a new reservation.

        Parameters:
            db (Session): Active database session.
            payload (ReservationCreate): Contains customer_id, table_id, date, and time.

        Returns:
            Reservation: Newly created reservation instance.
        """
        reservation = Reservation(
            customer_id=payload.customer_id,
            table_id=payload.table_id,
            date=payload.date,
            time=payload.time,
        )

        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation

    @staticmethod
    def get_reservation(db: Session, reservation_id: str):
        """
        Retrieve a reservation by ID.

        Parameters:
            db (Session): Active database session.
            reservation_id (str): Reservation ID.

        Returns:
            Reservation: Reservation instance if found.

        Raises:
            HTTPException: 404 if reservation not found.
        """
        reservation = db.query(Reservation).filter(
            Reservation.id == reservation_id
        ).first()

        if not reservation:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )

        return reservation

    @staticmethod
    def get_all_reservations(db: Session):
        """
        Retrieve all reservations.

        Parameters:
            db (Session): Active database session.

        Returns:
            list[Reservation]: All reservation records.
        """
        return db.query(Reservation).all()

    @staticmethod
    def update_reservation(db: Session, reservation_id: str, payload: ReservationUpdate):
        """
        Update an existing reservation.

        Parameters:
            db (Session): Active database session.
            reservation_id (str): ID of the reservation to update.
            payload (ReservationUpdate): Updated fields.

        Returns:
            Reservation: Updated reservation instance.

        Raises:
            HTTPException: 404 if reservation not found.
        """
        reservation = ReservationService.get_reservation(db, reservation_id)

        reservation.customer_id = payload.customer_id
        reservation.table_id = payload.table_id
        reservation.date = payload.date
        reservation.time = payload.time

        db.commit()
        db.refresh(reservation)
        return reservation

    @staticmethod
    def delete_reservation(db: Session, reservation_id: str):
        """
        Delete a reservation by ID.

        Parameters:
            db (Session): Active database session.
            reservation_id (str): Reservation ID to delete.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: 404 if reservation not found.
        """
        reservation = ReservationService.get_reservation(db, reservation_id)

        db.delete(reservation)
        db.commit()

        return {"message": "Reservation deleted successfully"}
