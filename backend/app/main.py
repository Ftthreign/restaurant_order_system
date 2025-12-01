from fastapi import FastAPI

from app.routers import (
    customers_router,
    menus_router,
    tables_router,
    reservations_router,
    orders_router,
    reports_router,
)

app = FastAPI(
    title="Restaurant Order System",
    description="Sistem pemesanan restoran dengan reservasi, menu, order, dan laporan.",
    version="1.0.0",
)


# Register all routers
app.include_router(customers_router)
app.include_router(menus_router)
app.include_router(tables_router)
app.include_router(reservations_router)
app.include_router(orders_router)
app.include_router(reports_router)


@app.get("/")
def root():
    return {"message": "Restaurant Order System API is running"}
