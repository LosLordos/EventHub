from fastapi import APIRouter, HTTPException, Depends
from ..domain.models import EventCreate, EventUpdate, EventOut
from ..services.catalog import CatalogService
from ..deps import get_catalog_service

router = APIRouter(prefix="/api/events", tags=["events"])


def _map(r) -> EventOut:
    return EventOut(
        event_id=r["EventId"],
        venue_id=r["VenueId"],
        title=r["Title"],
        starts_at=r["StartsAt"],
        capacity=r["Capacity"],
        sold_count=r["SoldCount"],
        ticket_price=float(r["TicketPrice"]),
        status=r["Status"],
        created_at=r["CreatedAt"],
    )


@router.get("", response_model=list[EventOut])
def list_events(svc: CatalogService = Depends(get_catalog_service)):
    return [_map(r) for r in svc.events.list()]


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, svc: CatalogService = Depends(get_catalog_service)):
    r = svc.events.get(event_id)
    if not r:
        raise HTTPException(404, "Event not found")
    return _map(r)


@router.post("", response_model=int)
def create_event(dto: EventCreate, svc: CatalogService = Depends(get_catalog_service)):
    try:
        return svc.events.create(
            venue_id=dto.venue_id,
            title=dto.title,
            starts_at=dto.starts_at,
            capacity=dto.capacity,
            ticket_price=dto.ticket_price,
            status=dto.status,
        )
    except Exception as e:
        raise HTTPException(400, f"Create failed: {e}")


@router.put("/{event_id}")
def update_event(event_id: int, dto: EventUpdate, svc: CatalogService = Depends(get_catalog_service)):
    n = svc.events.update(
        event_id,
        venue_id=dto.venue_id,
        title=dto.title,
        starts_at=dto.starts_at,
        capacity=dto.capacity,
        ticket_price=dto.ticket_price,
        status=dto.status,
    )
    if n == 0:
        raise HTTPException(404, "Nothing updated (not found or empty update)")
    return {"ok": True}


@router.delete("/{event_id}")
def delete_event(event_id: int, svc: CatalogService = Depends(get_catalog_service)):
    n = svc.events.delete(event_id)
    if n == 0:
        raise HTTPException(404, "Event not found")
    return {"ok": True}
