import json
from datetime import datetime
from typing import Union, cast
from requests import get
from requests.models import HTTPError, Response
from .APIQuery import APIQuery
from .jsonType import CredentialsJSON, DistanceMatrixJSON, PlaceJSON, ResponseJSON


class APIGateway:

    _API_KEY: str
    _CREDENTIALS_JSON: str
    _API_BASE_URL: str = "https://maps.googleapis.com/maps/api"
    _LOCATION_BIAS: Union[None, str] = None
    class RESTError(HTTPError): pass

    
    ### Dunder methods ###

    def __init__(self, credentials_json: str) -> None:
        self._CREDENTIALS_JSON = credentials_json
        self._get_api_key()

    
    ### Public methods ###
    
    def find_place(self, place: str) -> PlaceJSON:
        query: APIQuery = APIQuery(
            input=place,
            inputtype="textquery",
            fields="name,place_id,formatted_address,business_status,geometry"
            #language="en-GB",
            #locationbias=LONDON_LAT_LONG}
        )
        response_json: ResponseJSON = self._get("place/findplacefromtext", query)
        return cast(PlaceJSON, response_json)
        
    def find_distances(self, origins: list[str], destinations: list[str]) -> DistanceMatrixJSON:
        at = int(datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0).timestamp())
        print(f'arrival_time: [{type(at)}]', at)
        query: APIQuery = APIQuery(
            origins='|'.join('place_id:' + origin for origin in origins),
            destinations='|'.join('place_id:' + destination for destination in destinations),
            mode="transit",
            arrival_time=str(at),
            inputtype="textquery",
            fields="name,place_id,formatted_address,business_status,geometry",
            transit_mode="rail"
        )
        response_json: ResponseJSON = self._get("distancematrix", query)
        return cast(DistanceMatrixJSON, response_json)
    
    
    ### Private methods ###

    def _get(self, search_path: str, query: APIQuery) -> ResponseJSON:
        query.add_key(self._API_KEY)
        query.add_location_bias(self._LOCATION_BIAS)
        url: str = self._url_join(self._get_base_url(), search_path, "json")
        response: Response = get(url, params=query)
        print("URL: ", response.url)
        return self._validate_response(response)
    
    def _validate_response(self, response: Response) -> ResponseJSON:
        response.raise_for_status()
        response_json: ResponseJSON = response.json()
        if response_json['status'] != "OK":
            err_msg: str = "{code} ERROR: {status} for url: {url}".format(code=response.status_code,
                                                                          status=response_json['status'],
                                                                          url=response.url)
            raise self.RESTError(err_msg)
        return response_json
    
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
        if not -90 < lat_long_coords[0] <= 90:
            raise ValueError(f"The latitude '{lat_long_coords[0]}' must be between -90 and 90 degrees.")
        if not -180 < lat_long_coords[1] <= 180:
            raise ValueError(f"The latitude '{lat_long_coords[0]}' must be between -180 and 180 degrees.")
        self._LOCATION_BIAS = ','.join(str(c) for c in lat_long_coords)
    
