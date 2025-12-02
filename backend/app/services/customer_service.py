from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Customer
from app.schemas import (
    CustomerCreate,
    CustomerUpdate
)


class CustomerService:
    """
    Service class for managing Customer CRUD operations.
    Provides methods to create, retrieve, update, and delete customer records.
    """

    @staticmethod
    def create_customer(db: Session, payload: CustomerCreate):
        """
        Create a new customer.

        Parameters:
            db (Session): Active database session.
            payload (CustomerCreate): Input containing name and phone.

        Returns:
            Customer: Newly created customer instance.
        """
        customer = Customer(
            name=payload.name,
            phone=payload.phone
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def get_customer(db: Session, customer_id: str):
        """
        Retrieve a customer by ID.

        Parameters:
            db (Session): Active database session.
            customer_id (str): ID of the customer to retrieve.

        Returns:
            Customer: Customer instance if found.

        Raises:
            HTTPException: 404 if customer not found.
        """
        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return customer

    @staticmethod
    def get_all_customer(db: Session):
        """
        Retrieve all customers.

        Parameters:
            db (Session): Active database session.

        Returns:
            list[Customer]: All customer records.
        """
        return db.query(Customer).all()

    @staticmethod
    def update_customer(db: Session, customer_id: str, payload: CustomerUpdate):
        """
        Update an existing customer.

        Parameters:
            db (Session): Active database session.
            customer_id (str): ID of the customer to update.
            payload (CustomerUpdate): Updated name and phone.

        Returns:
            Customer: Updated customer instance.

        Raises:
            HTTPException: 404 if customer not found.
        """
        customer = CustomerService.get_customer(db, customer_id)

        customer.name = payload.name
        customer.phone = payload.phone

        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def delete_customer(db: Session, customer_id: str):
        """
        Delete a customer by ID.

        Parameters:
            db (Session): Active database session.
            customer_id (str): ID of the customer to delete.

        Returns:
            dict: Success message.

        Raises:
            HTTPException: 404 if customer not found.
        """
        customer = CustomerService.get_customer(db, customer_id)
        db.delete(customer)
        db.commit()

        return {"message": "Customer deleted successfully"}
