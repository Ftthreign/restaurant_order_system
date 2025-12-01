from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Table
from app.schemas import TableCreate, TableUpdate


class TableService:
    @staticmethod
    def create_table(
        db: Session,
        payload: TableCreate
    ):
        table = Table(
            table_number=payload.table_number,
            capacity=payload.capacity
        )

        db.add(table)
        db.commit()
        db.refresh(table)

        return table

    @staticmethod
    def get_table(
        db: Session,
        table_id: str
    ):
        table = db.query(Table).filter(Table.id == table_id).first()

        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        return table

    @staticmethod
    def get_all_tables(
        db: Session
    ):
        tables = db.query(Table).all()
        return tables

    @staticmethod
    def update_table(
        db: Session,
        table_id: str,
        payload: TableUpdate
    ):
        table = db.query(Table).filter(Table.id == table_id).first()

        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        table.table_number = payload.table_number
        table.capacity = payload.capacity

        db.commit()
        db.refresh(table)

        return table

    @staticmethod
    def delete_table(
        db: Session,
        table_id: str
    ):
        table = db.query(Table).filter(Table.id == table_id).first()

        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        db.delete(table)
        db.commit()

        return {"message": "Table deleted successfully"}
