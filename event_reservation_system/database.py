import mysql.connector
from mysql.connector import pooling
import json
import os

class Database:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        db_config = config['database']
        
        # Create a connection pool
        self._pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],

        )

    def get_connection(self):
        return self._pool.get_connection()

    def get_cursor(self, connection):
        return connection.cursor(dictionary=True)
