from sqlalchemy import text
from .base import BaseRepository

class EventRepository(BaseRepository):
    def list(self):
        with self.engine.connect() as conn:
            return list(conn.execute(text("""
                SELECT EventId, VenueId, Title, StartsAt, Capacity, SoldCount, TicketPrice, Status, CreatedAt
                FROM dbo.Event
                ORDER BY StartsAt
            """)).mappings())

    def get(self, event_id: int):
        with self.engine.connect() as conn:
            return conn.execute(text("""
                SELECT EventId, VenueId, Title, StartsAt, Capacity, SoldCount, TicketPrice, Status, CreatedAt
                FROM dbo.Event
                WHERE EventId=:id
            """), {"id": event_id}).mappings().first()

    def create(self, venue_id: int, title: str, starts_at, capacity: int, ticket_price: float, status: str):
        with self.engine.begin() as conn:
            return conn.execute(text("""
                INSERT INTO dbo.Event(VenueId, Title, StartsAt, Capacity, TicketPrice, Status)
                OUTPUT INSERTED.EventId
                VALUES (:vid,:t,:s,:cap,:p,:st)
            """), {"vid": venue_id, "t": title, "s": starts_at, "cap": capacity, "p": ticket_price, "st": status}).scalar_one()

    def update(self, event_id: int, **fields):
        allowed = {"venue_id":"VenueId","title":"Title","starts_at":"StartsAt","capacity":"Capacity","ticket_price":"TicketPrice","status":"Status"}
        sets, params = [], {"id": event_id}
        for k,v in fields.items():
            if v is None or k not in allowed:
                continue
            sets.append(f"{allowed[k]} = :{k}")
            params[k] = v
        if not sets:
            return 0
        with self.engine.begin() as conn:
            res = conn.execute(text(f"UPDATE dbo.Event SET {', '.join(sets)} WHERE EventId=:id"), params)
            return res.rowcount

    def delete(self, event_id: int):
        with self.engine.begin() as conn:
            res = conn.execute(text("DELETE FROM dbo.Event WHERE EventId=:id"), {"id": event_id})
            return res.rowcount
