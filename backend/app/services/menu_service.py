from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Menu
from app.schemas import MenuCreate, MenuUpdate


class MenuService:
    """
    Service class for managing Menu CRUD operations.
    Handles creation, retrieval, update, and deletion of menu items.
    """

    @staticmethod
    def create(db: Session, payload: MenuCreate):
        """
        Create a new menu item.

        Parameters:
            db (Session): Active database session.
            payload (MenuCreate): Contains name and price.

        Returns:
            Menu: Newly created menu item.
        """
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
        """
        Retrieve all menu items.

        Parameters:
            db (Session): Active database session.

        Returns:
            list[Menu]: List of all menus.
        """
        return db.query(Menu).all()

    @staticmethod
    def get(db: Session, menu_id: str):
        """
        Retrieve a menu item by ID.

        Parameters:
            db (Session): Active database session.
            menu_id (str): Menu ID.

        Returns:
            Menu: Menu item if found.

        Raises:
            HTTPException: 404 if menu not found.
        """
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(404, "Menu not found")
        return menu

    @staticmethod
    def update(db: Session, menu_id: str, payload: MenuUpdate):
        """
        Update an existing menu item.

        Parameters:
            db (Session): Active database session.
            menu_id (str): Menu ID.
            payload (MenuUpdate): Updated fields (name, price).

        Returns:
            Menu: Updated menu item.

        Raises:
            HTTPException: 404 if menu not found.
        """
        menu = MenuService.get(db, menu_id)

        menu.name = payload.name
        menu.price = payload.price

        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def delete(db: Session, menu_id: str):
        """
        Delete a menu item.

        Parameters:
            db (Session): Active database session.
            menu_id (str): Menu ID to delete.

        Returns:
            dict: Success message.

        Raises:
            HTTPException:
                - 404 if menu not found.
                - 400 if menu is referenced by order items.
        """
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(404, "Menu not found")

        if menu.order_items:
            raise HTTPException(
                400, "Menu cannot be deleted because it is used in order items")

        db.delete(menu)
        db.commit()
        return {"message": "Menu deleted"}
