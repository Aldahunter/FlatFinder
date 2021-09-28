import json
from typing import Union
import requests

class APIGateway:

    API_KEY: str
    CREDENTIALS_JSON: str

    def __init__(self, credentials_json: str) -> None:
        self.CREDENTIALS_JSON = credentials_json
        self.get_api_key()
    
    def _load_credentials(self) -> dict[str, str]:
        with open(self.CREDENTIALS_JSON) as json_file:
            return json.load(json_file)

    def get_api_key(self) -> None:
        self.API_KEY = self._load_credentials()['API_KEY']