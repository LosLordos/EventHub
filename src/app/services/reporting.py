from sqlalchemy import text
from sqlalchemy.engine import Engine

class ReportingService:
    def __init__(self, engine: Engine):
        self.engine = engine

    def attendance(self) -> list[dict]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT EventId, Title, StartsAt, Capacity, SoldCount, Remaining
                FROM dbo.v_event_attendance
                ORDER BY StartsAt
            """)).mappings().all()
            return [dict(r) for r in rows]

    def revenue(self) -> list[dict]:
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT EventId, Title, Revenue, PaymentsCount
                FROM dbo.v_event_revenue
                ORDER BY Revenue DESC
            """)).mappings().all()
            return [dict(r) for r in rows]

    def order_stats(self) -> dict:
        with self.engine.connect() as conn:
            r = conn.execute(text("""
                SELECT
                    MIN(CAST(TotalPrice AS float)) AS MinOrder,
                    MAX(CAST(TotalPrice AS float)) AS MaxOrder,
                    AVG(CAST(TotalPrice AS float)) AS AvgOrder,
                    COUNT(*) AS PaidOrders
                FROM dbo.TicketOrder
                WHERE Status = 'Paid'
            """)).mappings().first()
            if not r:
                return {"MinOrder": None, "MaxOrder": None, "AvgOrder": None, "PaidOrders": 0}
            return dict(r)
