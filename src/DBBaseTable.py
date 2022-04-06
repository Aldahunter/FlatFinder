from datetime import date, datetime, timezone
import string
from turtle import back
from typing import Type, cast
from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, String, TypeDecorator
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime
from sqlalchemy.sql.type_api import TypeEngine

### Declarative Base Class ###
Base: Type[object] = declarative_base()

def _base_repr(self: Base) -> str:
    exclude_attributes: list[str] = ['metadata', 'registry']
    columns: dict[str, str] = {attr:str(cast(object, self.__getattribute__(attr))) for attr in dir(self)
                                if (not attr.startswith("_")) and (attr not in exclude_attributes)}                   
    return f"<{cast(str, self.__getattribute__('__tablename__'))}(" \
        + ", ".join(f"{k}={v}" for (k, v) in columns.items()) \
        + ")>"
    # ToDo: update to for Base classes to just show their id

def _primary_column(sequence_name: str) -> Column[int]:
    return Column(Integer, cast(Sequence[str], Sequence(sequence_name)),
                  primary_key=True, index=True, unique=True, nullable=False)