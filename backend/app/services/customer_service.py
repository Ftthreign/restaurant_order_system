from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Customer
from app.schemas import (
    CustomerCreate,
    CustomerUpdate
)


class CustomerService:
    @staticmethod
    def create_customer(db: Session, payload: CustomerCreate):
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
        customer = db.query(Customer).filter(
            Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

    @staticmethod
    def get_all_customer(db: Session):
        return db.query(Customer).all()

    @staticmethod
    def update_customer(db: Session, customer_id: str, payload: CustomerUpdate):
        customer = CustomerService.get_customer(db, customer_id)

        customer.name = payload.name
        customer.phone = payload.phone

        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def delete_customer(db: Session, customer_id: str):
        customer = CustomerService.get_customer(db, customer_id)
        db.delete(customer)
        db.commit()
        return {"message": "Customer deleted successfully"}
