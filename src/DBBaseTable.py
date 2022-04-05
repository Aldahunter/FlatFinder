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

def _primary_column(sequence_name: str) -> Column[int]:
    return Column(Integer, cast(Sequence[str], Sequence(sequence_name)),
                  primary_key=True, index=True, unique=True, nullable=False)

class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: datetime, dialect: object) -> datetime:
        if value is not None:
            if not value.tzinfo:
                raise TypeError(f"Got naive datetime while timezone-aware is expected: {value}")
            value = value.astimezone(timezone.utc).replace(
                tzinfo=None
            )
        return value

    def process_result_value(self, value: datetime, dialect: object) -> datetime:
        if value is not None:
            value = value.replace(tzinfo=timezone.utc)
        return value


# class utcnow(expression.FunctionElement[DateTime]):
#     type: DateTime = DateTime() # type: ignore
#     inherit_cache: bool = True

# @compiles(utcnow, 'postgresql')  # type: ignore
# def pg_utcnow(element: object, compiler: object, **kw: object) -> str:
#     return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
# @compiles(utcnow, 'mssql')  # type: ignore
# def ms_utcnow(element: object, compiler: object, **kw: object) -> str:
#     return "GETUTCDATE()"