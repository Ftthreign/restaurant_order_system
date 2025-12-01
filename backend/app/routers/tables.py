from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TableCreate, TableUpdate, TableResponse
from app.services.table_service import TableService

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.post("/", response_model=TableResponse)
def create_table(payload: TableCreate, db: Session = Depends(get_db)):
    return TableService.create_table(db, payload)


@router.get("/", response_model=list[TableResponse])
def get_tables(db: Session = Depends(get_db)):
    return TableService.get_all_tables(db)


@router.get("/{table_id}", response_model=TableResponse)
def get_table(table_id: str, db: Session = Depends(get_db)):
    return TableService.get_table(db, table_id)


@router.put("/{table_id}", response_model=TableResponse)
def update_table(table_id: str, payload: TableUpdate, db: Session = Depends(get_db)):
    return TableService.update_table(db, table_id, payload)


@router.delete("/{table_id}")
def delete_table(table_id: str, db: Session = Depends(get_db)):
    return TableService.delete_table(db, table_id)
