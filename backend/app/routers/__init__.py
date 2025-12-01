from .customers import router as customers_router
from .menu import router as menus_router
from .tables import router as tables_router
from .reservations import router as reservations_router
from .orders import router as orders_router
from .reports import router as reports_router

__all__ = [
    "customers_router",
    "menus_router",
    "tables_router",
    "reservations_router",
    "orders_router",
    "reports_router",
]
