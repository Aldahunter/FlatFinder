import logging
from typing import Type, TypeVar
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine

from src.DBBaseTable import Base
from src.DBTables import Entries

_T = TypeVar('_T')

class DBShield:
    engine: Engine
    session: Session
    sessionmaker: sessionmaker
    base: Type[object]
    entries: Entries
    meta: MetaData

    _logger: logging.Logger
    _logger_name: str = "sqlalchemy.engine"
    _logger_level: int = logging.INFO
    _logger_file_name: str = "database.log"
    _logger_file_handler: logging.FileHandler
    _logger_formatter: logging.Formatter


    def __init__(self, path: str, show_sql_commands: bool = False):
        self._setup_logger()

        self.engine = create_engine('sqlite:///data/FlatFinder.db', echo=show_sql_commands)
        self.base = Base
        self.entries = Entries()
        self.meta = self.base.metadata
        self.meta.create_all(self.engine)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
    
    def _setup_logger(self) -> None:
        self._logger_file_handler = logging.FileHandler(self._logger_file_name)
        self._logger_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                                   datefmt='%Y-%m-%d %H:%M:%S')
        self._logger_file_handler.setFormatter(self._logger_formatter)
        self._logger = logging.getLogger(self._logger_name)
        self._logger.addHandler(self._logger_file_handler)
        self._logger.setLevel(self._logger_level)
    
    def commit(self) -> None:
        self.session.commit()
    
    def add(self, *entries: _T) -> None:
        self.session.add_all(entries)
        self.commit()
    
    # Cant do Query[_T]
    def query(self, entry: Type[_T], *args: object, **kwargs: object) -> Query:
        return self.session.query(entry, *args, **kwargs)