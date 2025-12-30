from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..services.catalog import CatalogService
from ..services.ticketing import TicketingService
from ..services.reporting import ReportingService
from ..deps import get_catalog_service, get_ticketing_service, get_reporting_service

router = APIRouter(tags=["ui"])
templates = Jinja2Templates(directory="src/app/templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# ---------------- Customers ----------------

@router.get("/customers")
def customers_list(request: Request, svc: CatalogService = Depends(get_catalog_service)):
    customers = svc.customers.list()
    return templates.TemplateResponse("customers_list.html", {"request": request, "customers": customers})

@router.post("/customers/create")
def customers_create(
    request: Request,
    email: str = Form(...),
    full_name: str = Form(...),
    phone: str = Form(None),
    svc: CatalogService = Depends(get_catalog_service),
):
    svc.customers.create(email=email, full_name=full_name, phone=phone, is_active=True)
    return RedirectResponse(url="/customers", status_code=303)

# ---------------- Venues ----------------

@router.get("/venues")
def venues_list(request: Request, svc: CatalogService = Depends(get_catalog_service)):
    venues = svc.venues.list()
    return templates.TemplateResponse("venues_list.html", {"request": request, "venues": venues})

@router.post("/venues/create")
def venues_create(
    request: Request,
    name: str = Form(...),
    city: str = Form(...),
    address: str = Form(...),
    svc: CatalogService = Depends(get_catalog_service),
):
    svc.venues.create(name=name, city=city, address=address, is_active=True)
    return RedirectResponse(url="/venues", status_code=303)

# ---------------- Events ----------------

@router.get("/events")
def events_list(request: Request, svc: CatalogService = Depends(get_catalog_service)):
    events = svc.events.list()
    venues = svc.venues.list()
    return templates.TemplateResponse("events_list.html", {"request": request, "events": events, "venues": venues})

@router.post("/events/create")
def events_create(
    request: Request,
    venue_id: int = Form(...),
    title: str = Form(...),
    starts_at: str = Form(...),  # ISO string
    capacity: int = Form(...),
    ticket_price: float = Form(...),
    status: str = Form(...),
    svc: CatalogService = Depends(get_catalog_service),
):
    dt = datetime.fromisoformat(starts_at)
    svc.events.create(venue_id=venue_id, title=title, starts_at=dt, capacity=capacity, ticket_price=ticket_price, status=status)
    return RedirectResponse(url="/events", status_code=303)

# ---------------- Buy tickets (Phase 4–5) ----------------

@router.get("/buy")
def buy_form(request: Request, svc: CatalogService = Depends(get_catalog_service)):
    events = [e for e in svc.events.list() if e["Status"] == "Published"]
    customers = svc.customers.list()
    return templates.TemplateResponse("order_create.html", {
        "request": request,
        "events": events,
        "customers": customers,
        "error": None,
        "success": None
    })

@router.post("/buy")
def buy_submit(
    request: Request,
    event_id: int = Form(...),
    customer_id: int = Form(...),
    quantity: int = Form(...),
    method: str = Form(...),
    cat: CatalogService = Depends(get_catalog_service),
    svc: TicketingService = Depends(get_ticketing_service),
):
    events = [e for e in cat.events.list() if e["Status"] == "Published"]
    customers = cat.customers.list()

    try:
        res = svc.buy_tickets(event_id=event_id, customer_id=customer_id, quantity=quantity, method=method)
        return templates.TemplateResponse("order_create.html", {
            "request": request,
            "events": events,
            "customers": customers,
            "error": None,
            "success": f"Nákup OK. OrderId={res.order_id}, PaymentId={res.payment_id}"
        })
    except Exception as e:
        return templates.TemplateResponse("order_create.html", {
            "request": request,
            "events": events,
            "customers": customers,
            "error": str(e),
            "success": None
        })

# ---------------- Reports (Phase 6) ----------------

@router.get("/reports")
def reports_page(request: Request, svc: ReportingService = Depends(get_reporting_service)):
    attendance = svc.attendance()
    revenue = svc.revenue()
    stats = svc.order_stats()
    return templates.TemplateResponse("reports.html", {
        "request": request,
        "attendance": attendance,
        "revenue": revenue,
        "stats": stats
    })
