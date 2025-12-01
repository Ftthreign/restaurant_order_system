from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Reservation
from app.schemas import ReservationCreate, ReservationUpdate


class ReservationService:
    @staticmethod
    def create_reservation(db: Session, payload: ReservationCreate):
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
        reservation = db.query(Reservation).filter(
            Reservation.id == reservation_id).first()
        if not reservation:
            raise HTTPException(
                status_code=404, detail="Reservation not found")
        return reservation

    @staticmethod
    def get_all_reservations(db: Session):
        return db.query(Reservation).all()

    @staticmethod
    def update_reservation(db: Session, reservation_id: str, payload: ReservationUpdate):
        reservation = ReservationService.get_reservation(db, reservation_id)

        if not reservation:
            raise HTTPException(
                status_code=404, detail="Reservation not found")

        reservation.customer_id = payload.customer_id
        reservation.table_id = payload.table_id
        reservation.date = payload.date
        reservation.time = payload.time

        db.commit()
        db.refresh(reservation)

        return reservation

    @staticmethod
    def delete_reservation(db: Session, reservation_id: str):
        reservation = ReservationService.get_reservation(db, reservation_id)

        if not reservation:
            raise HTTPException(
                status_code=404, detail="Reservation not found")

        db.delete(reservation)
        db.commit()

        return {"message": "Reservation deleted successfully"}
