from APIGateway import APIGateway

class FlatFinder:

    DATABASE_NAME="FlatFinder.db"
    APIGW=None

    def __init__(self) -> None:
        DB = sl.connect(self.DATABASE_NAME)
        quit()
        self.APIGW = APIGateway("credentials.json")

if __name__ == "__main__":
    FlatFinder()