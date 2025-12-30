from sqlalchemy.engine import Engine
from ..repositories.customers import CustomerRepository
from ..repositories.venues import VenueRepository
from ..repositories.events import EventRepository

class CatalogService:
    def __init__(self, engine: Engine):
        self.customers = CustomerRepository(engine)
        self.venues = VenueRepository(engine)
        self.events = EventRepository(engine)
