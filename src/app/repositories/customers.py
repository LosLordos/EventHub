from sqlalchemy import text
from .base import BaseRepository

class CustomerRepository(BaseRepository):
    def list(self):
        with self.engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT CustomerId, Email, FullName, Phone, IsActive, CreatedAt
                FROM dbo.Customer
                ORDER BY CreatedAt DESC
            """)).mappings().all()
            return list(rows)

    def get(self, customer_id: int):
        with self.engine.connect() as conn:
            row = conn.execute(text("""
                SELECT CustomerId, Email, FullName, Phone, IsActive, CreatedAt
                FROM dbo.Customer
                WHERE CustomerId = :id
            """), {"id": customer_id}).mappings().first()
            return row

    def create(self, email: str, full_name: str, phone: str | None, is_active: bool):
        with self.engine.begin() as conn:
            return conn.execute(text("""
                INSERT INTO dbo.Customer(Email, FullName, Phone, IsActive)
                OUTPUT INSERTED.CustomerId
                VALUES (:email, :name, :phone, :active)
            """), {"email": email, "name": full_name, "phone": phone, "active": 1 if is_active else 0}).scalar_one()

    def update(self, customer_id: int, full_name: str | None, phone: str | None, is_active: bool | None):
        sets = []
        params = {"id": customer_id}
        if full_name is not None:
            sets.append("FullName = :name"); params["name"] = full_name
        if phone is not None:
            sets.append("Phone = :phone"); params["phone"] = phone
        if is_active is not None:
            sets.append("IsActive = :active"); params["active"] = 1 if is_active else 0

        if not sets:
            return 0

        with self.engine.begin() as conn:
            res = conn.execute(text(f"""
                UPDATE dbo.Customer SET {", ".join(sets)}
                WHERE CustomerId = :id
            """), params)
            return res.rowcount

    def delete(self, customer_id: int):
        with self.engine.begin() as conn:
            res = conn.execute(text("DELETE FROM dbo.Customer WHERE CustomerId = :id"), {"id": customer_id})
            return res.rowcount
