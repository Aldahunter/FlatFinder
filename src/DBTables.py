from typing import Type, cast
from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

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
    return Column(Integer, cast(Sequence[str], Sequence(sequence_name)), primary_key=True)


### Declarative Extensions ###
class DBTables:

    class Location(Base):
        __tablename__: str = 'locations'
        __repr__ = _base_repr
    
        id = _primary_column('location_id_seq')
        lat = Column(Float(6))
        long = Column(Float(6))
        
    class Viewport(Base):
        __tablename__: str = 'viewports'
        __repr__ = _base_repr

        id: Column[int] = _primary_column('viewport_id_seq')
        northeast: Column[object] = Column(ForeignKey('locations.id'))
        southwest: Column[object] = Column(ForeignKey('locations.id'))
        
    class Geometry(Base):
        __tablename__: str = 'geometries'
        __repr__ = _base_repr

        id = _primary_column('geometry_id_seq')
        location_id: Column[object] = Column(ForeignKey('locations.id'))
        viewport_id: Column[object] = Column(ForeignKey('viewports.id'))

    class Place(Base):
        __tablename__: str = 'places'
        __repr__ = _base_repr

        id = _primary_column('place_id_seq')
        name: Column[object] = Column(String(200), index=True)
        formatted_address: Column[object] = Column(String(200))
        geometry_id: Column[object] = Column(ForeignKey('geometries.id'))
