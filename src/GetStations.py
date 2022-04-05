# type: ignore
from datetime import datetime, timedelta
from typing import Optional
from src.DBShield import DBShield
from src.DBTables import Place, PlaceQuery
from src.JsonToDbParser import JsonToDbParser
from src.jsonType import PlaceCandidateJSON, PlaceResponseJSON
from src.APIGateway import APIGateway
from os.path import dirname, join as pathJoin, isfile
from json import dumps, load, loads
from sqlalchemy.orm.query import Query


class GetStations:

    file_path: str
    database: DBShield
    jsn_parser: JsonToDbParser

    def __init__(self, database: DBShield, stations_file: str):
        if not isfile(stations_file):
            raise IOError(f"The Station Names file is not accessible: '{stations_file}'")
        self.file_path = stations_file
        self.database = database
        self.jsn_parser = JsonToDbParser(database)
    
    def add_stations(self, gateway: APIGateway) -> None:
        stations: list[str] = self._parse_stations(self._get_file_lines())
        self.uptodate_benchmark: datetime = datetime.utcnow() - timedelta(weeks=52)

        for station in stations:
            if not self._is_station_uptodate(station):
                print(f"#### Querying API for '{station}'")
                self._add_station(station, gateway)
            else:
                print(f"### Did not add '{station}' as is uptodate")
            print(f"### Added '{station}'")
    
    def _get_file_lines(self) -> list[str]:
        with open(self.file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    
    def _is_stations_suffix(self, line: str) -> bool:            
        if line.startswith('#'):
            self.station_suffix: str = line.replace('#', '').strip() 
            return True
        return False
    
    def _parse_stations(self, lines: list[str]) -> list[str]:
        return [f"{line} {self.station_suffix}" for line in lines
                if not self._is_stations_suffix(line)]
    
    def _get_place_response(self, station: str, gateway: APIGateway) -> PlaceResponseJSON:
        place_json: PlaceResponseJSON = gateway.find_place(station)

        ### Delete me after run ###
        if len(place_json["candidates"]) > 1:
            str_list: str = str([c["place_id"] for c in place_json["candidates"]])
            print(str_list)
            with open(pathJoin(r"C:\DATA\repos\FlatFinder\resources", "multiple_candidates.txt"), "a") as file:
                file.write(str_list + '\n')
        for c in place_json["candidates"]:
            place_id: str = c["place_id"]
            with open(pathJoin(r"C:\DATA\repos\FlatFinder\resources", f"{place_id}.txt"), "w") as file:
                file.write(dumps(c))
        ### Delete me after run ###
        return place_json

    def _get_place_query(self, station: str, place: Place) -> PlaceQuery:
        return self.database.entries.PlaceQuery(query=station, place=place) # type: ignore
    
    def _is_station_uptodate(self, station: str) -> bool:
        query: Optional[PlaceQuery] = self.database.query(PlaceQuery).join(Place)\
                                                   .filter(PlaceQuery.query == station,
                                                           Place.last_updated >= self.uptodate_benchmark)\
                                                   .first()
        return query is not None
    
    
    def _add_station(self, station: str, gateway: APIGateway) -> None:
        print(f"Searching for '{station}'.")

        place_json: PlaceCandidateJSON = self._get_place_response(station, gateway)["candidates"][0]
        print(place_json)

        place: Place = self.jsn_parser.build_place_entry(place_json)#, station)
        place_query: PlaceQuery = self._get_place_query(station, place)
        self.database.add(place, place_query)

