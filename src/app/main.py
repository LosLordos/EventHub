from fastapi import FastAPI

from .api.customers import router as customers_router
from .api.venues import router as venues_router
from .api.events import router as events_router
from .api.orders import router as orders_router
from .api.reports import router as reports_router
from .ui.ui import router as ui_router

app = FastAPI(title="EventHub")

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(ui_router)
app.include_router(customers_router)
app.include_router(venues_router)
app.include_router(events_router)
app.include_router(orders_router)
app.include_router(reports_router)
