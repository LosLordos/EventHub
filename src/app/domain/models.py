from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

# ---------------- Customers ----------------

class CustomerCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=140)
    phone: Optional[str] = Field(default=None, max_length=30)
    is_active: bool = True

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=140)
    phone: Optional[str] = Field(default=None, max_length=30)
    is_active: Optional[bool] = None

class CustomerOut(BaseModel):
    customer_id: int
    email: EmailStr
    full_name: str
    phone: Optional[str]
    is_active: bool
    created_at: datetime

# ---------------- Venues ----------------

class VenueCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    city: str = Field(min_length=2, max_length=80)
    address: str = Field(min_length=2, max_length=160)
    is_active: bool = True

class VenueUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    city: Optional[str] = Field(default=None, min_length=2, max_length=80)
    address: Optional[str] = Field(default=None, min_length=2, max_length=160)
    is_active: Optional[bool] = None

class VenueOut(BaseModel):
    venue_id: int
    name: str
    city: str
    address: str
    is_active: bool

# ---------------- Events ----------------

class EventCreate(BaseModel):
    venue_id: int
    title: str = Field(min_length=2, max_length=160)
    starts_at: datetime
    capacity: int = Field(ge=0)
    ticket_price: float = Field(ge=0)
    status: str = Field(pattern="^(Draft|Published|Cancelled|Finished)$")

class EventUpdate(BaseModel):
    venue_id: Optional[int] = None
    title: Optional[str] = Field(default=None, min_length=2, max_length=160)
    starts_at: Optional[datetime] = None
    capacity: Optional[int] = Field(default=None, ge=0)
    ticket_price: Optional[float] = Field(default=None, ge=0)
    status: Optional[str] = Field(default=None, pattern="^(Draft|Published|Cancelled|Finished)$")

class EventOut(BaseModel):
    event_id: int
    venue_id: int
    title: str
    starts_at: datetime
    capacity: int
    sold_count: int
    ticket_price: float
    status: str
    created_at: datetime

# ---------------- Ticket purchase (Phase 4–5) ----------------

class TicketPurchaseIn(BaseModel):
    event_id: int
    customer_id: int
    quantity: int = Field(gt=0)
    method: str = Field(pattern="^(Card|Cash|BankTransfer)$")

class TicketPurchaseOut(BaseModel):
    ok: bool = True
    order_id: int
    payment_id: int
    message: str

# ---------------- Reports (Phase 6) ----------------

class AttendanceRow(BaseModel):
    event_id: int
    title: str
    starts_at: datetime
    capacity: int
    sold_count: int
    remaining: int

class RevenueRow(BaseModel):
    event_id: int
    title: str
    revenue: float
    payments_count: int

class OrderStatsOut(BaseModel):
    min_order: Optional[float]
    max_order: Optional[float]
    avg_order: Optional[float]
    paid_orders: int
