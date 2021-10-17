import json
from typing import Union
import requests

class APIGateway:

    _API_KEY: str
    _CREDENTIALS_JSON: str

    def __init__(self, credentials_json: str) -> None:
        self._CREDENTIALS_JSON = credentials_json
        self._get_api_key()
    
    def _load_credentials(self) -> dict[str, str]:
        with open(self._CREDENTIALS_JSON) as json_file:
            return json.load(json_file)

    def _get_api_key(self) -> None:
        self._API_KEY = self._load_credentials()['API_KEY']