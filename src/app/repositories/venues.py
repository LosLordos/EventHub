from sqlalchemy import text
from .base import BaseRepository

class VenueRepository(BaseRepository):
    def list(self):
        with self.engine.connect() as conn:
            return list(conn.execute(text("""
                SELECT VenueId, Name, City, Address, IsActive
                FROM dbo.Venue
                ORDER BY Name
            """)).mappings())

    def get(self, venue_id: int):
        with self.engine.connect() as conn:
            return conn.execute(text("""
                SELECT VenueId, Name, City, Address, IsActive
                FROM dbo.Venue
                WHERE VenueId = :id
            """), {"id": venue_id}).mappings().first()

    def create(self, name: str, city: str, address: str, is_active: bool):
        with self.engine.begin() as conn:
            return conn.execute(text("""
                INSERT INTO dbo.Venue(Name, City, Address, IsActive)
                OUTPUT INSERTED.VenueId
                VALUES (:n,:c,:a,:active)
            """), {"n": name, "c": city, "a": address, "active": 1 if is_active else 0}).scalar_one()

    def update(self, venue_id: int, name: str | None, city: str | None, address: str | None, is_active: bool | None):
        sets = []
        params = {"id": venue_id}
        if name is not None: sets.append("Name = :n"); params["n"] = name
        if city is not None: sets.append("City = :c"); params["c"] = city
        if address is not None: sets.append("Address = :a"); params["a"] = address
        if is_active is not None: sets.append("IsActive = :active"); params["active"] = 1 if is_active else 0
        if not sets:
            return 0
        with self.engine.begin() as conn:
            res = conn.execute(text(f"UPDATE dbo.Venue SET {', '.join(sets)} WHERE VenueId=:id"), params)
            return res.rowcount

    def delete(self, venue_id: int):
        with self.engine.begin() as conn:
            res = conn.execute(text("DELETE FROM dbo.Venue WHERE VenueId=:id"), {"id": venue_id})
            return res.rowcount
