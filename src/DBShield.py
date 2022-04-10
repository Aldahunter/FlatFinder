import logging
from typing import Type, TypeVar
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine
from src.APIGateway import APIGateway

from src.database.DBBaseTable import Base

_T = TypeVar('_T')

class DBShield:
    engine: Engine
    session: Session
    sessionmaker: sessionmaker
    base: Type[object]
    meta: MetaData

    _logger: logging.Logger
    _logger_name: str = "sqlalchemy.engine"
    _logger_level: int = logging.INFO
    _logger_file_name: str = "database.log"
    _logger_file_handler: logging.FileHandler
    _logger_formatter: logging.Formatter

    _station_integrity_file_path: str = r"C:\DATA\repos\FlatFinder\resources\ListOfStations.txt"


    def __init__(self, path: str, show_sql_commands: bool = False):
        self._setup_logger()

        self.engine = create_engine('sqlite:///data/FlatFinder.db', echo=show_sql_commands)
        self.base = Base
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
    
    def ensure_station_entgrity(self, gateway: APIGateway) -> None:
        from src.database.StationIntegrityCache import StationIntegrityCache
        StationIntegrityCache(self._station_integrity_file_path, self, gateway).ensure_data_integrity()
    
    def commit(self) -> None:
        self.session.commit()
    
    def add(self, *entries: _T) -> None:
        self.session.add_all(entries)
        self.commit()
    
    def query(self, entry: Type[_T], *args: object, **kwargs: object) -> 'Query[_T]':
        return self.session.query(entry, *args, **kwargs)