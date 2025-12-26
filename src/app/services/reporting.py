from sqlalchemy import text
from sqlalchemy.engine import Engine

class ReportingService:
    def __init__(self, engine: Engine):
        self.engine = engine

    def attendance(self):
        with self.engine.connect() as conn:
            return list(conn.execute(text("SELECT * FROM dbo.v_event_attendance ORDER BY StartsAt")).mappings())

    def revenue(self):
        with self.engine.connect() as conn:
            return list(conn.execute(text("SELECT * FROM dbo.v_event_revenue ORDER BY Revenue DESC")).mappings())

    def summary_stats(self):
        # agregace přes 3+ tabulek: Event + TicketOrder + Payment
        with self.engine.connect() as conn:
            row = conn.execute(text("""
                SELECT
                  MIN(o.TotalPrice) AS MinOrder,
                  MAX(o.TotalPrice) AS MaxOrder,
                  AVG(o.TotalPrice) AS AvgOrder
                FROM dbo.TicketOrder o
                WHERE o.Status='Paid'
            """)).mappings().first()
            return row or {"MinOrder": None, "MaxOrder": None, "AvgOrder": None}
