from sqlalchemy.engine import Engine

class BaseRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
