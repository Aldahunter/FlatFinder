
from os.path import isfile

from src.PlaceCache import PlaceCache


class StationIntegrityCache:

    file_path: str
    station_cache_caller: PlaceCache

    def __init__(self, stations_file: str):
        if not isfile(stations_file):
            raise IOError(f"The Station Names file is not accessible: '{stations_file}'")
        self.file_path = stations_file
        self.station_cache_caller = PlaceCache()

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

    def get_stations(self) -> list[str]:
        station_queries: list[str] = self._parse_stations(self._get_file_lines())
        for station_query in station_queries:
            self.station_cache_caller.get_place(station_query)