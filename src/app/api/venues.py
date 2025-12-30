from fastapi import APIRouter, HTTPException, Depends
from ..domain.models import VenueCreate, VenueUpdate, VenueOut
from ..services.catalog import CatalogService
from ..deps import get_catalog_service

router = APIRouter(prefix="/api/venues", tags=["venues"])


def _map(r) -> VenueOut:
    return VenueOut(
        venue_id=r["VenueId"],
        name=r["Name"],
        city=r["City"],
        address=r["Address"],
        is_active=bool(r["IsActive"]),
    )


@router.get("", response_model=list[VenueOut])
def list_venues(svc: CatalogService = Depends(get_catalog_service)):
    return [_map(r) for r in svc.venues.list()]


@router.get("/{venue_id}", response_model=VenueOut)
def get_venue(venue_id: int, svc: CatalogService = Depends(get_catalog_service)):
    r = svc.venues.get(venue_id)
    if not r:
        raise HTTPException(404, "Venue not found")
    return _map(r)


@router.post("", response_model=int)
def create_venue(dto: VenueCreate, svc: CatalogService = Depends(get_catalog_service)):
    try:
        return svc.venues.create(dto.name, dto.city, dto.address, dto.is_active)
    except Exception as e:
        raise HTTPException(400, f"Create failed: {e}")


@router.put("/{venue_id}")
def update_venue(venue_id: int, dto: VenueUpdate, svc: CatalogService = Depends(get_catalog_service)):
    n = svc.venues.update(venue_id, dto.name, dto.city, dto.address, dto.is_active)
    if n == 0:
        raise HTTPException(404, "Nothing updated (not found or empty update)")
    return {"ok": True}


@router.delete("/{venue_id}")
def delete_venue(venue_id: int, svc: CatalogService = Depends(get_catalog_service)):
    n = svc.venues.delete(venue_id)
    if n == 0:
        raise HTTPException(404, "Venue not found")
    return {"ok": True}
