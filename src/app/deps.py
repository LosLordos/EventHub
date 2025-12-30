from .config import load_settings
from .db import create_db_engine

from .services.catalog import CatalogService
from .services.ticketing import TicketingService
from .services.reporting import ReportingService

settings = load_settings("config.yaml")
engine = create_db_engine(settings)

def get_catalog_service() -> CatalogService:
    return CatalogService(engine)

def get_ticketing_service() -> TicketingService:
    return TicketingService(engine)

def get_reporting_service() -> ReportingService:
    return ReportingService(engine)
