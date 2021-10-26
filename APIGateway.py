import json
import os
from typing import NewType, Union, cast
import requests
from requests.models import HTTPError, Request, Response
from jsonType import CredentialsJSON, PlaceJSON, ResponseJSON

class APIGateway:

    _API_KEY: str
    _CREDENTIALS_JSON: str
    _API_BASE_URL: str = "https://maps.googleapis.com/maps/api"
    _LOCATION_BIAS: Union[None, str] = None
    class RESTError(HTTPError): pass
    

    def __init__(self, credentials_json: str) -> None:
        self._CREDENTIALS_JSON = credentials_json
        self._get_api_key()

    def _get(self, search_path: str, query: 'APIGateway.APIQUERY') -> ResponseJSON:
        url: str = self._url_join(self._get_base_url(), search_path, "json")
        response: Response = requests.get(url, params=query)
        self._raise_error_for_status(response)
        response_json: ResponseJSON = response.json()
        return response_json
    
    def find_place(self, place: str) -> PlaceJSON:
        query: 'APIGateway.APIQUERY' = self.APIQUERY(self,
            input=place,
            inputtype="textquery",
            fields="name,place_id,formatted_address,business_status,geometry"
            #language="en-GB",
            #locationbias=LONDON_LAT_LONG}
        )
        response_json: ResponseJSON = self._get("place/findplacefromtext", query)
        return cast(PlaceJSON, response_json)
    
    def _load_credentials(self) -> CredentialsJSON:
        with open(self._CREDENTIALS_JSON) as json_file:
            credentials_json: CredentialsJSON = json.load(json_file)
        return credentials_json

    def _get_api_key(self) -> None:
        self._API_KEY = self._load_credentials()['API_KEY']
    
    def _get_base_url(self) -> str:
        return self._API_BASE_URL
    
    def _url_join(self, *args: str) -> str:
        return r"/".join(s.strip('/') for s in args)
    
    def add_location_bias(self, lat_long_coords: tuple[float, float]) -> None:
        if -90 < lat_long_coords[0] <= 90:
            raise TypeError(f"The latitude '{lat_long_coords[0]}' must be between -90 and 90 degrees.")
        if 180 < lat_long_coords[1] <= 180:
            raise TypeError(f"The latitude '{lat_long_coords[0]}' must be between -180 and 180 degrees.")
        self._LOCATION_BIAS = ','.join(str(c) for c in lat_long_coords)
    
    class APIQUERY(dict[str, str]): 
        def __init__(self, parent: 'APIGateway', **kwargs: str) -> None:
            self._parent: APIGateway = parent
            super().__init__(**kwargs)
            self._add_key()
            self._add_location_bias()
    
        def _add_key(self) -> None:
            if (self.get("key", None) is None) and (self._parent._API_KEY is not None):
                self['key'] = self._parent._API_KEY
    
        def _add_location_bias(self) -> None:
            if (self.get("locationbias", None) is None) and (self._parent._LOCATION_BIAS is not None):
                self['key'] = self._parent._LOCATION_BIAS
    
    def _raise_error_for_status(self, response: Response) -> None:
        response.raise_for_status()
        response_json: ResponseJSON = response.json()
        if response_json['status'] != "OK":
            err_msg: str = "{code} ERROR: {status} for url: {url}".format(code=response.status_code,
                                                                          status=response_json['status'],
                                                                          url=response.url)
            raise self.RESTError(err_msg)