import json

class FlatFinder:

    API_KEY=None
    CREDENTIALS_JSON="credentials.json"

    def __init__(self) -> None:
        self.get_api_key()
        quit()
    
    def _load_credentials(self):
        with open(self.CREDENTIALS_JSON) as json_file:
            return json.load(json_file)

    def get_api_key(self):
        self.API_KEY = self._load_credentials()['API_KEY']

if __name__ == "__main__":
    FlatFinder()