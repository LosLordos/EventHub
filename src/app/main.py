from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .config import load_settings
from .db import create_db_engine
from .services.ticketing import TicketingService
from .services.reporting import ReportingService
from .services.importing import ImportingService

app = FastAPI(title="EventHub")
templates = Jinja2Templates(directory="src/app/templates")

settings = load_settings("config.yaml")
engine = create_db_engine(settings)

ticketing = TicketingService(engine)
reporting = ReportingService(engine)
importing = ImportingService(engine, settings.import_max_rows)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("layout.html", {"request": request, "content": "EventHub běží."})

@app.post("/api/buy")
def buy(event_id: int, customer_id: int, quantity: int, method: str):
    try:
        res = ticketing.buy_tickets(event_id=event_id, customer_id=customer_id, quantity=quantity, method=method)
        return {"ok": True, "order_id": res.order_id, "payment_id": res.payment_id}
    except Exception as e:
        return JSONResponse(status_code=400, content={"ok": False, "error": str(e)})

@app.get("/api/reports/attendance")
def report_attendance():
    return reporting.attendance()

@app.get("/api/reports/revenue")
def report_revenue():
    return reporting.revenue()
s