from os.path import dirname, join as pathJoin
from src.DBShield import DBShield
from src.APIGateway import APIGateway

class FlatFinder:

    _APIGW: APIGateway
    _DBSHLD: DBShield
    _BASE_DIR: str = dirname(__file__)
    _LONDON_LAT_LONG: tuple[float, float]=(51.50735400298231,-0.12775683066393959)

    def __init__(self) -> None:
        self._APIGW = APIGateway(pathJoin(self._BASE_DIR, "credentials.json"))
        self._DBSHLD = DBShield(pathJoin(self._BASE_DIR, "FlatFinder.db"))

if __name__ == "__main__":
    print("Starting FlatFinder...")
    FlatFinder()
    print("FlatFinder Complete.")