from datetime import datetime, timedelta
from typing import Optional

from src.DBShield import DBShield
from src.DBTables import Place, PlaceQuery
from src.JsonToDbParser import JsonToDbParser
from src.PlaceCaller import PlaceCaller
from src.jsonType import PlaceCandidateJSON
from src.APIGateway import APIGateway


class PlaceCache:

    database: DBShield
    json_parser: JsonToDbParser
    place_caller: PlaceCaller
            
    def __init__(self, database: DBShield, gateway: APIGateway, cache_expiry: int = 52):
        self.database = database
        self.place_caller = PlaceCaller(gateway)
        self.json_parser = JsonToDbParser()
        self.expiry_date: datetime = datetime.utcnow() - timedelta(weeks=cache_expiry)
    
    def _parse_place_json(self, place_json: PlaceCandidateJSON) -> Place:
        place: Place = self.database.query(Place).filter_by(place_id=place_json['place_id']).first()
        if place is None:
            place = self.json_parser.build_place_entry(place_json)
        return place
    
    def _get_place_query(self, query: str) -> Optional[PlaceQuery]:
        return(self.database.query(PlaceQuery)
            .join(Place)
            .filter(PlaceQuery.search_query == query,
                    Place.last_updated >= self.expiry_date)
            .first())

    def get_place(self, place: str) -> Place:
        place_query: Optional[PlaceQuery] = self._get_place_query(place)
        
        if place_query is None:
            place_json: PlaceCandidateJSON = self.place_caller.get_place(place)
            place: Place = self._parse_place_json(place_json)
            self.database.add(place, PlaceQuery(search_query=place, place=place))
            return place
        return place_query.place