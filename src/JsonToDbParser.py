from ctypes import cast
from sqlalchemy.exc import IntegrityError
from typing import TypeGuard

from sqlalchemy.sql.schema import Column, Table

from src.DBShield import DBShield
from src.DBBaseTable import Base
from src.DBTables import Geometry, LatLongCoords, Place, PlaceQuery, Viewport
from src.jsonType import PlaceCandidateJSON

class JsonToDbParser:

    database: DBShield

    def __init__(self, database: DBShield) -> None:
        self.database = database    

    def build_place_entry(self, place_json: PlaceCandidateJSON) -> Place:
        print('@@@', type(place_json), place_json)
        place: Place = self.database.entries.Place( # type: ignore
            place_id = place_json['place_id'],
            name = place_json['name'],
            formatted_address = place_json.get('formatted_address'),
            business_status = place_json.get('business_status'),
            geometry = self.database.entries.Geometry( # type: ignore
                    location = self.database.entries.LatLongCoords( # type: ignore
                            lat = place_json.get('geometry', {}).get('location', {}).get('lat'),
                            lng = place_json.get('geometry', {}).get('location', {}).get('lng')),
                    viewport = self.database.entries.Viewport( # type: ignore
                        northeast = self.database.entries.LatLongCoords( # type: ignore
                            lat = place_json.get('geometry', {}).get('viewport', {}).get('northeast', {}).get('lat'),
                            lng = place_json.get('geometry', {}).get('viewport', {}).get('northeast', {}).get('lng')
                        ),
                        southwest = self.database.entries.LatLongCoords( # type: ignore
                            lat = place_json.get('geometry', {}).get('viewport', {}).get('southwest', {}).get('lat'),
                            lng = place_json.get('geometry', {}).get('viewport', {}).get('southwest', {}).get('lng')
                        )))#,
            #place_query = self.database.datums.place_query(query=query)
        ) # type: ignore
        try:
            print('### Commiting')
            self.database.add(place)
            self.database.commit()
        except (IntegrityError, Exception) as e:
            print(f'### Rollingback due to "{e}" [{type(e)}]')
            self.database.session.rollback()
            place = self.database.query(self.database.entries.Place).filter_by(place_id=place_json['place_id']).first()
        return place
        
    


    ### Get DBTable columns, see which are foreign keys
    ### Get JSON keys, see which are other JSONs
    ### Align columns with keys
    ### Create Table Entries filled with JSON values (lowest rungs first)