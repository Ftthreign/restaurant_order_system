from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Menu
from app.schemas import MenuCreate, MenuUpdate


class MenuService:

    @staticmethod
    def create(db: Session, payload: MenuCreate):
        menu = Menu(
            name=payload.name,
            price=payload.price
        )
        db.add(menu)
        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def get_all(db: Session):
        return db.query(Menu).all()

    @staticmethod
    def get(db: Session, menu_id: str):
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(404, "Menu not found")
        return menu

    @staticmethod
    def update(db: Session, menu_id: str, payload: MenuUpdate):
        menu = MenuService.get(db, menu_id)

        menu.name = payload.name
        menu.price = payload.price

        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def delete(db: Session, menu_id: str):
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(404, "Menu not found")

        if menu.order_items:
            raise HTTPException(
                400, "Menu cannot be deleted because it is used in order items")

        db.delete(menu)
        db.commit()
        return {"message": "Menu deleted"}
