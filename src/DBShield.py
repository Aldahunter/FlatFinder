from typing import Type, cast
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

from src.DBTables import Base, DBTables

class DBShield:
    db: Engine
    session: sessionmaker
    base: Type[object]
    meta: MetaData
    tables: DBTables

    def __init__(self, path: str):
        db = create_engine('sqlite:///data/FlatFinder.db', echo = True)
        session = sessionmaker(bind = db)
        base = Base
        meta = base.metadata
        tables = DBTables
        meta.create_all(db)

