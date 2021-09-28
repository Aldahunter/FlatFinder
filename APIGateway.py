import json
import requests

class APIGateway:

    API_KEY=None
    CREDENTIALS_JSON=None

    def __init__(self, credentials_json) -> None:
        self.CREDENTIALS_JSON = credentials_json
        self.get_api_key()
    
    def _load_credentials(self):
        with open(self.CREDENTIALS_JSON) as json_file:
            return json.load(json_file)

    def get_api_key(self):
        self.API_KEY = self._load_credentials()['API_KEY']