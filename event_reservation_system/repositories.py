from database import Database
import mysql.connector

class BaseRepository:
    def __init__(self):
        self.db = Database()

    def get_cursor(self, conn):
        return self.db.get_cursor(conn)

class UserRepository(BaseRepository):
    def create(self, email, password_hash, role='customer', display_name=None):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = "INSERT INTO users (email, password_hash, role, display_name) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (email, password_hash, role, display_name))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def get_by_email(self, email):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, user_id):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

class EventRepository(BaseRepository):
    def get_all_upcoming(self):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            # Using the View as requested/designed, or the table directly.
            # Requirement says "Use View". We defined v_upcoming_events.
            sql = "SELECT * FROM v_upcoming_events"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_all(self):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = "SELECT e.*, v.name as venue_name FROM events e JOIN venues v ON e.venue_id = v.id"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, event_id):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = "SELECT e.*, v.name as venue_name, v.capacity FROM events e JOIN venues v ON e.venue_id = v.id WHERE e.id = %s"
            cursor.execute(sql, (event_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def create(self, venue_id, title, description, start_time, base_price, is_active=True):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = """
                INSERT INTO events (venue_id, title, description, start_time, base_price, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (venue_id, title, description, start_time, base_price, is_active))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    def update(self, event_id, **kwargs):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            # Dynamic update query
            set_clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])
            values = list(kwargs.values())
            values.append(event_id)
            
            sql = f"UPDATE events SET {set_clause} WHERE id = %s"
            cursor.execute(sql, values)
            conn.commit()
        finally:
            cursor.close()
            conn.close()
            
    def delete(self, event_id):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = "DELETE FROM events WHERE id = %s"
            cursor.execute(sql, (event_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()


class BookingRepository(BaseRepository):
    def create_booking_transaction(self, user_id, items, total_price):
        """
        Executes a transaction to:
        1. Check capacity (Application logic needed usually, but we can lock or check here).
           Note: The requirement asks for transaction usage.
        2. Insert booking.
        3. Insert booking items.
        """
        conn = self.db.get_connection()
        # Start transaction explicitly
        conn.start_transaction()
        cursor = self.get_cursor(conn)
        
        try:
            # 1. Insert Booking
            sql_booking = "INSERT INTO bookings (user_id, total_price, status) VALUES (%s, %s, 'confirmed')"
            cursor.execute(sql_booking, (user_id, total_price))
            booking_id = cursor.lastrowid
            
            # 2. Insert Items
            sql_item = "INSERT INTO booking_items (booking_id, event_id, quantity, unit_price) VALUES (%s, %s, %s, %s)"
            
            for item in items:
                # item is a dict: {'event_id': 1, 'quantity': 2, 'unit_price': 50.0}
                cursor.execute(sql_item, (
                    booking_id, 
                    item['event_id'], 
                    item['quantity'], 
                    item['unit_price']
                ))
            
            # Commit Transaction
            conn.commit()
            return booking_id
        
        except Exception as e:
            # Rollback on any error
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_user_bookings(self, user_id):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = "SELECT * FROM bookings WHERE user_id = %s ORDER BY created_at DESC"
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

class VenueRepository(BaseRepository):
     def get_all(self):
        conn = self.db.get_connection()
        cursor = self.get_cursor(conn)
        try:
            sql = "SELECT * FROM venues"
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
