from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import MenuCreate, MenuUpdate, MenuResponse
from app.services.menu_service import MenuService

router = APIRouter(prefix="/menus", tags=["Menus"])


@router.post("/", response_model=MenuResponse)
def create_menu(payload: MenuCreate, db: Session = Depends(get_db)):
    return MenuService.create(db, payload)


@router.get("/", response_model=list[MenuResponse])
def get_menus(db: Session = Depends(get_db)):
    return MenuService.get_all(db)


@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu(menu_id: str, db: Session = Depends(get_db)):
    return MenuService.get(db, menu_id)


@router.put("/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: str, payload: MenuUpdate, db: Session = Depends(get_db)):
    return MenuService.update(db, menu_id, payload)


@router.delete("/{menu_id}")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    return MenuService.delete(db, menu_id)
