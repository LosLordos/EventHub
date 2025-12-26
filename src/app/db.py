from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from .config import Settings

def create_db_engine(settings: Settings) -> Engine:
    try:
        return create_engine(settings.connection_string, pool_pre_ping=True, future=True)
    except Exception as e:
        raise RuntimeError("Nelze vytvořit DB engine. Zkontroluj connection string a ODBC driver.") from e
