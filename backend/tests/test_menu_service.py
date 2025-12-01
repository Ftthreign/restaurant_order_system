import pytest
from fastapi import HTTPException
from app.schemas import MenuCreate, MenuUpdate
from app.services.menu_service import MenuService
from app.models import Menu


def test_create_menu(test_db):
    payload = MenuCreate(name="Nasi Goreng", price=15000)

    menu = MenuService.create(test_db, payload)

    assert menu.id is not None
    assert menu.name == "Nasi Goreng"
    assert menu.price == 15000


def test_get_all_menu(test_db):
    MenuService.create(test_db, MenuCreate(name="A", price=1000))
    MenuService.create(test_db, MenuCreate(name="B", price=2000))

    result = MenuService.get_all(test_db)

    assert len(result) == 2


def test_get_menu(test_db):
    created = MenuService.create(
        test_db, MenuCreate(name="Sate Ayam", price=20000)
    )

    menu = MenuService.get(test_db, created.id)

    assert menu.name == "Sate Ayam"
    assert menu.price == 20000


def test_get_menu_not_found(test_db):
    with pytest.raises(HTTPException) as exc:
        MenuService.get(test_db, "not-found-id")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Menu not found"


def test_update_menu(test_db):
    created = MenuService.create(
        test_db, MenuCreate(name="Bakso", price=12000)
    )

    updated = MenuService.update(
        test_db,
        created.id,
        MenuUpdate(name="Bakso Urat", price=15000)
    )

    assert updated.name == "Bakso Urat"
    assert updated.price == 15000


def test_delete_menu(test_db):
    created = MenuService.create(
        test_db, MenuCreate(name="Es Teh", price=5000)
    )

    result = MenuService.delete(test_db, created.id)

    assert result["message"] == "Menu deleted"

    with pytest.raises(HTTPException):
        MenuService.get(test_db, created.id)
