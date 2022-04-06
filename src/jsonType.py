from typing import TypeVar, TypedDict, cast

### Generic Classes ###
KT = TypeVar('KT'); VT = TypeVar('VT')

### Base API Return JSONs
class LatLongCoords(TypedDict):
    lat: float
    lng: float

class Viewport(TypedDict):
    northeast: LatLongCoords
    southwest: LatLongCoords

class Geometry(TypedDict):
    location: LatLongCoords
    viewport: Viewport


### API Return JSONs
class ResponseJSON(TypedDict):
    status: str

class PlaceResponseJSON(ResponseJSON):
    candidates: list['PlaceCandidateJSON']
class PlaceCandidateJSON(TypedDict, total=False):
    business_status: str
    formatted_address: str
    geometry: Geometry
    name: str
    place_id: str

### Credentials JSON
class CredentialsJSON(TypedDict):
    API_KEY: str