from typing import Union
from DBShield import DBShield
from APIGateway import APIGateway

class FlatFinder:

    _APIGW: APIGateway
    _DBSHLD: DBShield
    _LONDON_LAT_LONG: tuple[float, float]=(51.50735400298231,-0.12775683066393959)

    def __init__(self) -> None:
        self._APIGW = APIGateway("credentials.json")
        self._DBSHLD = DBShield("FlatFinder.db")

if __name__ == "__main__":
    print("Starting FlatFinder...")
    FlatFinder()
    print("FlatFinder Complete.")