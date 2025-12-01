from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/daily-sales")
def daily_sales(db: Session = Depends(get_db)):
    return ReportService.daily_sales(db)


@router.get("/menu-rank")
def menu_rank(db: Session = Depends(get_db)):
    return ReportService.menu_rank(db)
