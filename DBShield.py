import sqlite3 as sl
from sqlite3.dbapi2 import Connection

class DBShield:

    _DATABASE_NAME: str
    _DB: Connection

    def __init__(self, database_name: str) -> None:
        self._DATABASE_NAME = database_name
        self._connect_to_database()
    
    def _connect_to_database(self) -> None:
        self._DB = sl.connect(self._DATABASE_NAME)