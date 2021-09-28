import sqlite3 as sl
from sqlite3.dbapi2 import Connection

class DBShield:

    DATABASE_NAME: str
    DB: Connection

    def __init__(self, database_name: str) -> None:
        self.DATABASE_NAME = database_name
        self.connect_to_database()
    
    def connect_to_database(self) -> None:
        self.DB = sl.connect(self.DATABASE_NAME)