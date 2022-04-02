from src.DBBaseTable import _base_repr, Base, _primary_column
from turtle import back
from typing import Type, cast
from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, String
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class LatLongCoords(Base):
    __tablename__: str = 'lat_long_coords'
    __repr__ = _base_repr

    id = _primary_column('lat_long_coords_id_seq')
    lat = Column(Float(6))
    lng = Column(Float(6))


    
class Viewport(Base):
    __tablename__: str = 'viewports'
    __repr__ = _base_repr

    id: Column[int] = _primary_column('viewport_id_seq')
    northeast_id: Column[object] = Column(ForeignKey('lat_long_coords.id'))
    southwest_id: Column[object] = Column(ForeignKey('lat_long_coords.id'))

    geometry: 'Geometry' = relationship('Geometry', back_populates='viewport') # type: ignore
    northeast : 'LatLongCoords' = relationship('LatLongCoords', foreign_keys=northeast_id) # type: ignore
    southwest : 'LatLongCoords' = relationship('LatLongCoords', foreign_keys=southwest_id) # type: ignore
    
class Geometry(Base):
    __tablename__: str = 'geometries'
    __repr__ = _base_repr

    id = _primary_column('geometry_id_seq')
    location_id: Column[object] = Column(ForeignKey('lat_long_coords.id'))
    viewport_id: Column[object] = Column(ForeignKey('viewports.id'))

    place: 'Place' = relationship('Place', back_populates='geometry') # type: ignore
    location : 'LatLongCoords' = relationship('LatLongCoords') # type: ignore
    viewport : 'Viewport' = relationship('Viewport', back_populates='geometry') # type: ignore



class Place(Base):
    __tablename__: str = 'places'
    __repr__ = _base_repr

    id = _primary_column('place_id_seq')
    place_id: Column[object] = Column(String(200), index=True)
    name: Column[object] = Column(String(200), index=True)
    formatted_address: Column[object] = Column(String(200))
    business_status: Column[object] = Column(String(12))
    geometry_id: Column[object] = Column(ForeignKey('geometries.id'))

    geometry: 'Geometry' = relationship('Geometry', back_populates='place') # type: ignore
