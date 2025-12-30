from fastapi import APIRouter, HTTPException, Depends
from ..domain.models import TicketPurchaseIn, TicketPurchaseOut
from ..services.ticketing import TicketingService
from ..deps import get_ticketing_service

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/buy", response_model=TicketPurchaseOut)
def buy(dto: TicketPurchaseIn, svc: TicketingService = Depends(get_ticketing_service)):
    try:
        res = svc.buy_tickets(
            event_id=dto.event_id,
            customer_id=dto.customer_id,
            quantity=dto.quantity,
            method=dto.method,
        )
        return TicketPurchaseOut(order_id=res.order_id, payment_id=res.payment_id, message="Nákup proběhl úspěšně.")
    except ValueError as e:
        raise HTTPException(400, str(e))
    except RuntimeError as e:
        raise HTTPException(409, str(e))
    except Exception:
        raise HTTPException(500, "Neočekávaná chyba při nákupu. Zkus to znovu.")
