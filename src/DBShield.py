from typing import Type
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

from src.DBBaseTable import Base
import src.DBTables as tables

class DBShield:
    engine: Engine
    session: Session
    sessionmaker: sessionmaker
    base: Type[object]
    meta: MetaData

    def __init__(self, path: str):
        self.engine = create_engine('sqlite:///data/FlatFinder.db', echo = True)
        self.base = Base
        self.tables = tables
        self.meta = self.base.metadata
        self.meta.create_all(self.engine)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        

