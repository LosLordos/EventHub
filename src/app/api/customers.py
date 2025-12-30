from fastapi import APIRouter, HTTPException, Depends
from ..domain.models import CustomerCreate, CustomerUpdate, CustomerOut
from ..services.catalog import CatalogService
from ..deps import get_catalog_service

router = APIRouter(prefix="/api/customers", tags=["customers"])

def _map(row) -> CustomerOut:
    return CustomerOut(
        customer_id=row["CustomerId"],
        email=row["Email"],
        full_name=row["FullName"],
        phone=row["Phone"],
        is_active=bool(row["IsActive"]),
        created_at=row["CreatedAt"],
    )

@router.get("", response_model=list[CustomerOut])
def list_customers(svc: CatalogService = Depends(get_catalog_service)):
    return [_map(r) for r in svc.customers.list()]

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, svc: CatalogService = Depends(get_catalog_service)):
    r = svc.customers.get(customer_id)
    if not r:
        raise HTTPException(404, "Customer not found")
    return _map(r)

@router.post("", response_model=int)
def create_customer(dto: CustomerCreate, svc: CatalogService = Depends(get_catalog_service)):
    try:
        return svc.customers.create(dto.email, dto.full_name, dto.phone, dto.is_active)
    except Exception as e:
        raise HTTPException(400, f"Create failed: {e}")

@router.put("/{customer_id}")
def update_customer(customer_id: int, dto: CustomerUpdate, svc: CatalogService = Depends(get_catalog_service)):
    n = svc.customers.update(customer_id, dto.full_name, dto.phone, dto.is_active)
    if n == 0:
        raise HTTPException(404, "Nothing updated (not found or empty update)")
    return {"ok": True}

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, svc: CatalogService = Depends(get_catalog_service)):
    n = svc.customers.delete(customer_id)
    if n == 0:
        raise HTTPException(404, "Customer not found")
    return {"ok": True}
