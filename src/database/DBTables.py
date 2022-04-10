# type: ignore [syntax]

from datetime import datetime
from src.database.DBBaseTable import _base_repr, Base, _primary_column
from sqlalchemy import TIMESTAMP, Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now as sql_now, current_timestamp as sql_current_timestamp

class LatLongCoords(Base):
    __tablename__: str = 'lat_long_coords'
    __repr__ = _base_repr

    id: int = _primary_column('lat_long_coords_id_seq')
    lat: float = Column(Float(6), nullable=False)
    lng: float = Column(Float(6), nullable=False)
    
class Viewport(Base):
    __tablename__: str = 'viewports'
    __repr__ = _base_repr

    id: int = _primary_column('viewport_id_seq')
    northeast_id: int = Column(ForeignKey('lat_long_coords.id'), nullable=False)
    southwest_id: int = Column(ForeignKey('lat_long_coords.id'), nullable=False)

    geometry: 'Geometry' = relationship('Geometry', back_populates='viewport')
    northeast : 'LatLongCoords' = relationship('LatLongCoords', foreign_keys=northeast_id)
    southwest : 'LatLongCoords' = relationship('LatLongCoords', foreign_keys=southwest_id)
    
class Geometry(Base):
    __tablename__: str = 'geometries'
    __repr__ = _base_repr

    id: int = _primary_column('geometry_id_seq')
    location_id: int = Column(ForeignKey('lat_long_coords.id'), nullable=False)
    viewport_id: int = Column(ForeignKey('viewports.id'), nullable=False)

    place: 'Place' = relationship('Place', back_populates='geometry')
    location: 'LatLongCoords' = relationship('LatLongCoords')
    viewport: 'Viewport' = relationship('Viewport', back_populates='geometry')

class PlaceQuery(Base):
    __tablename__: str = 'place_queries'
    __repr__ = _base_repr

    id: int = _primary_column('place_query_id_seq')
    search_query: str = Column(String(200), index=True, unique=True, nullable=False)
    place_id: int = Column(ForeignKey('places.id'), nullable=False)

    place: 'Place' = relationship('Place', back_populates='place_query')

class Place(Base):
    __tablename__: str = 'places'
    __repr__ = _base_repr

    id: int = _primary_column('place_id_seq') 
    place_id: str = Column(String(200), index=True, unique=True, nullable=False) 
    name: str = Column(String(200), index=True, nullable=False) 
    formatted_address: str = Column(String(200)) 
    business_status: str = Column(String(12)) 
    geometry_id: int = Column(ForeignKey('geometries.id'))
    last_updated: datetime = Column(TIMESTAMP, server_default=sql_now(), onupdate=sql_current_timestamp())

    geometry: 'Geometry' = relationship('Geometry', back_populates='place')
    place_query: 'PlaceQuery' = relationship('PlaceQuery', order_by=PlaceQuery.id, back_populates='place')