import csv
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.engine import Engine

class ImportingService:
    def __init__(self, engine: Engine, max_rows: int):
        self.engine = engine
        self.max_rows = max_rows

    def import_customers_csv(self, path: str) -> dict:
        ok, errors = 0, []
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if len(rows) > self.max_rows:
            return {"ok": 0, "errors": [f"Soubor má {len(rows)} řádků, limit je {self.max_rows}."]}

        with self.engine.begin() as conn:
            for i, r in enumerate(rows, start=2):
                email = (r.get("Email") or "").strip()
                name = (r.get("FullName") or "").strip()
                phone = (r.get("Phone") or "").strip() or None
                if not email or "@" not in email:
                    errors.append(f"Řádek {i}: Neplatný Email.")
                    continue
                if not name:
                    errors.append(f"Řádek {i}: Chybí FullName.")
                    continue
                try:
                    conn.execute(text("""
                        IF NOT EXISTS (SELECT 1 FROM dbo.Customer WHERE Email=:email)
                        INSERT INTO dbo.Customer(Email, FullName, Phone) VALUES (:email, :name, :phone)
                    """), {"email": email, "name": name, "phone": phone})
                    ok += 1
                except Exception as e:
                    errors.append(f"Řádek {i}: DB chyba ({type(e).__name__}).")

        return {"ok": ok, "errors": errors}

    def import_events_csv(self, path: str) -> dict:
        ok, errors = 0, []
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if len(rows) > self.max_rows:
            return {"ok": 0, "errors": [f"Soubor má {len(rows)} řádků, limit je {self.max_rows}."]}

        with self.engine.begin() as conn:
            for i, r in enumerate(rows, start=2):
                try:
                    venue_id = int((r.get("VenueId") or "").strip())
                    title = (r.get("Title") or "").strip()
                    starts = datetime.fromisoformat((r.get("StartsAt") or "").strip())
                    cap = int((r.get("Capacity") or "").strip())
                    price = float((r.get("TicketPrice") or "").strip())
                    status = (r.get("Status") or "").strip()
                    if status not in ("Draft", "Published", "Cancelled", "Finished"):
                        raise ValueError("Status mimo enum")
                    if not title:
                        raise ValueError("Chybí Title")

                    conn.execute(text("""
                        INSERT INTO dbo.Event(VenueId, Title, StartsAt, Capacity, TicketPrice, Status)
                        VALUES (:vid,:t,:s,:c,:p,:st)
                    """), {"vid": venue_id, "t": title, "s": starts, "c": cap, "p": price, "st": status})
                    ok += 1
                except Exception as e:
                    errors.append(f"Řádek {i}: Neplatná data ({type(e).__name__}).")

        return {"ok": ok, "errors": errors}
