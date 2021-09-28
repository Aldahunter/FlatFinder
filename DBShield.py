import sqlite3 as sl

class DBShield:

    DATABASE_NAME=None
    DB=None

    def __init__(self, database_name) -> None:
        self.DATABASE_NAME = database_name
        self.connect_to_database()
    
    def connect_to_database(self):
        self.DB = sl.connect(self.DATABASE_NAME)