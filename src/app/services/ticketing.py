from dataclasses import dataclass
from sqlalchemy import text
from sqlalchemy.engine import Engine

@dataclass(frozen=True)
class PurchaseResult:
    order_id: int
    payment_id: int

class TicketingService:
    def __init__(self, engine: Engine):
        self.engine = engine

    def buy_tickets(self, *, event_id: int, customer_id: int, quantity: int, method: str) -> PurchaseResult:
        if quantity <= 0:
            raise ValueError("Množství musí být > 0.")
        if method not in ("Card", "Cash", "BankTransfer"):
            raise ValueError("Neplatná metoda platby.")

        with self.engine.begin() as conn:
            # 1) Zamkni akci (UPDLOCK) a ověř kapacitu
            row = conn.execute(text("""
                SELECT EventId, Capacity, SoldCount, TicketPrice, Status
                FROM dbo.Event WITH (UPDLOCK, ROWLOCK)
                WHERE EventId = :eid
            """), {"eid": event_id}).mappings().first()

            if not row:
                raise RuntimeError("Akce neexistuje.")
            if row["Status"] != "Published":
                raise RuntimeError("Lístky lze kupovat jen pro Published akce.")
            remaining = int(row["Capacity"]) - int(row["SoldCount"])
            if quantity > remaining:
                raise RuntimeError(f"Nedostatečná kapacita. Zbývá {remaining} míst.")

            unit_price = float(row["TicketPrice"])

            # 2) Vlož objednávku (TicketOrder)
            order_id = conn.execute(text("""
                INSERT INTO dbo.TicketOrder(EventId, CustomerId, Quantity, UnitPrice, Status)
                OUTPUT INSERTED.TicketOrderId
                VALUES (:eid, :cid, :qty, :price, 'Paid')
            """), {"eid": event_id, "cid": customer_id, "qty": quantity, "price": unit_price}).scalar_one()

            # 3) Aktualizuj sold count (constraint hlídá SoldCount<=Capacity)
            conn.execute(text("""
                UPDATE dbo.Event
                SET SoldCount = SoldCount + :qty
                WHERE EventId = :eid
            """), {"qty": quantity, "eid": event_id})

            # 4) Vlož platbu
            amount = unit_price * quantity
            payment_id = conn.execute(text("""
                INSERT INTO dbo.Payment(TicketOrderId, Amount, Method, IsRefund)
                OUTPUT INSERTED.PaymentId
                VALUES (:oid, :amount, :method, 0)
            """), {"oid": order_id, "amount": amount, "method": method}).scalar_one()

            # 5) Zapiš účastníka (idempotentně)
            conn.execute(text("""
                IF NOT EXISTS (SELECT 1 FROM dbo.EventParticipant WHERE EventId=:eid AND CustomerId=:cid)
                INSERT INTO dbo.EventParticipant(EventId, CustomerId) VALUES (:eid, :cid)
            """), {"eid": event_id, "cid": customer_id})

            return PurchaseResult(order_id=order_id, payment_id=payment_id)
