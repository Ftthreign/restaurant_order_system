import pytest
from fastapi import HTTPException

from app.schemas import CustomerCreate, CustomerUpdate
from app.services.customer_service import CustomerService


def test_create_customer(test_db):
    payload = CustomerCreate(name="Budi", phone="08123456")
    customer = CustomerService.create_customer(test_db, payload)

    assert customer.id is not None
    assert customer.name == "Budi"
    assert customer.phone == "08123456"


def test_get_customer(test_db):
    payload = CustomerCreate(name="Andi", phone="089999")
    created = CustomerService.create_customer(test_db, payload)

    customer = CustomerService.get_customer(test_db, created.id)
    assert customer.name == "Andi"


def test_get_customer_not_found(test_db):
    with pytest.raises(HTTPException) as exc:
        CustomerService.get_customer(test_db, "tidak-ada-id")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Customer not found"


def test_get_all_customer(test_db):
    CustomerService.create_customer(
        test_db, CustomerCreate(name="A", phone="1"))
    CustomerService.create_customer(
        test_db, CustomerCreate(name="B", phone="2"))

    customers = CustomerService.get_all_customer(test_db)
    assert len(customers) == 2


def test_update_customer(test_db):
    created = CustomerService.create_customer(
        test_db, CustomerCreate(name="Citra", phone="0987")
    )

    updated = CustomerService.update_customer(
        test_db,
        created.id,
        CustomerUpdate(name="Citra Baru", phone="0000")
    )

    assert updated.name == "Citra Baru"
    assert updated.phone == "0000"


def test_delete_customer(test_db):
    created = CustomerService.create_customer(
        test_db, CustomerCreate(name="Doni", phone="7777")
    )

    result = CustomerService.delete_customer(test_db, created.id)
    assert result["message"] == "Customer deleted successfully"

    with pytest.raises(HTTPException):
        CustomerService.get_customer(test_db, created.id)
