from typing import Type, cast
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

from src.DBTables import Base, DBTables

class DBShield:
    engine: Engine
    session: Session
    sessionmaker: sessionmaker
    base: Type[object]
    meta: MetaData
    tables: Type[DBTables]

    def __init__(self, path: str):
        self.engine = create_engine('sqlite:///data/FlatFinder.db', echo = True)
        self.base = Base
        self.tables = DBTables
        self.meta = self.base.metadata
        self.meta.create_all(self.engine)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        

