from typing import TypeGuard

from sqlalchemy.sql.schema import Column, Table

from src.DBShield import DBShield
from src.DBBaseTable import Base
from src.DBTables import Geometry, LatLongCoords, Place, Viewport
from src.jsonType import PlaceCandidate


class TableClass:
    __table__: Table

db = DBShield(r'C:\DATA\repos\FlatFinder\data\FlatFinder.db')

class JsonToDbParser:

    def _is_foreign_key(self, column: Column[object]) -> bool:
        num_foreign_keys = len(column.foreign_keys)
        if num_foreign_keys == 0:
            return False
        elif num_foreign_keys == 1:
            return True
        else:
            raise NotImplementedError
    
    def _is_table_class(self, possible_table: Base) -> TypeGuard[TableClass]:
        return hasattr(possible_table, '__table__')
    
    def _get_table(self, table_class: Base) -> Table:
        if self._is_table_class(table_class):
            return table_class.__table__
        raise TypeError(f"The input is not a table class: '{table_class}'")

    def _get_columns(self, table: Table) -> list[Column[object]]:
        return list(table.c)
    

    def build_place_entry(self, place_json: PlaceCandidate):
        place = db.tables.Place(
            place_id = place_json['place_id'],
            name = place_json['name'],
            formatted_address = place_json['formatted_address'],
            business_status = place_json['business_status'],
            geometry = db.tables.Geometry(
                    location = db.tables.LatLongCoords(
                            lat = place_json['geometry']['location']['lat'],
                            lng = place_json['geometry']['location']['lng']),
                    viewport = db.tables.Viewport(
                        northeast = db.tables.LatLongCoords(
                            lat = place_json['geometry']['viewport']['northeast']['lat'],
                            lng = place_json['geometry']['viewport']['northeast']['lng']
                        ),
                        southwest = db.tables.LatLongCoords(
                            lat = place_json['geometry']['viewport']['southwest']['lat'],
                            lng = place_json['geometry']['viewport']['southwest']['lng']
                        ),
                    )))
        
    


    ### Get DBTable columns, see which are foreign keys
    ### Get JSON keys, see which are other JSONs
    ### Align columns with keys
    ### Create Table Entries filled with JSON values (lowest rungs first)