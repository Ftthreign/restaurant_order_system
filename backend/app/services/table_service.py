from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Table
from app.schemas import TableCreate, TableUpdate


class TableService:
    """
    Service class for managing Table CRUD operations.
    Handles creation, retrieval, update, and deletion of table records.
    """

    @staticmethod
    def create_table(db: Session, payload: TableCreate):
        """
        Create a new table.

        Parameters:
            db (Session): Active database session.
            payload (TableCreate): Contains table_number and capacity.

        Returns:
            Table: Newly created table instance.
        """
        table = Table(
            table_number=payload.table_number,
            capacity=payload.capacity
        )

        db.add(table)
        db.commit()
        db.refresh(table)
        return table

    @staticmethod
    def get_table(db: Session, table_id: str):
        """
        Retrieve a table by ID.

        Parameters:
            db (Session): Active database session.
            table_id (str): Table ID.

        Returns:
            Table: Table instance if found.

        Raises:
            HTTPException: 404 if table not found.
        """
        table = db.query(Table).filter(Table.id == table_id).first()

        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        return table

    @staticmethod
    def get_all_tables(db: Session):
        """
        Retrieve all tables.

        Parameters:
            db (Session): Active database session.

        Returns:
            list[Table]: List of all tables.
        """
        return db.query(Table).all()

    @staticmethod
    def update_table(db: Session, table_id: str, payload: TableUpdate):
        """
        Update an existing table.

        Parameters:
            db (Session): Active database session.
            table_id (str): ID of the table to update.
            payload (TableUpdate): Updated fields (table_number, capacity).

        Returns:
            Table: Updated table instance.

        Raises:
            HTTPException: 404 if table not found.
        """
        table = db.query(Table).filter(Table.id == table_id).first()

        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        table.table_number = payload.table_number
        table.capacity = payload.capacity

        db.commit()
        db.refresh(table)
        return table

    @staticmethod
    def delete_table(db: Session, table_id: str):
        """
        Delete a table by ID.

        Parameters:
            db (Session): Active database session.
            table_id (str): Table ID to delete.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: 404 if table not found.
        """
        table = db.query(Table).filter(Table.id == table_id).first()

        if not table:
            raise HTTPException(status_code=404, detail="Table not found")

        db.delete(table)
        db.commit()

        return {"message": "Table deleted successfully"}
