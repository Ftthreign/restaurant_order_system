from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    ReservationCreate,
    ReservationUpdate,
    ReservationResponse,
)
from app.services.reservation_service import ReservationService

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=ReservationResponse)
def create_reservation(payload: ReservationCreate, db: Session = Depends(get_db)):
    return ReservationService.create_reservation(db, payload)


@router.get("/", response_model=list[ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    return ReservationService.get_all_reservations(db)


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    return ReservationService.get_reservation(db, reservation_id)


@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(reservation_id: str, payload: ReservationUpdate, db: Session = Depends(get_db)):
    return ReservationService.update_reservation(db, reservation_id, payload)


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    return ReservationService.delete_reservation(db, reservation_id)
