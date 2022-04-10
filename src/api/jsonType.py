from typing import TypeVar, TypedDict

### Generic Classes ###
KT = TypeVar('KT'); VT = TypeVar('VT')

### Base API Return JSONs
class LatLongCoordsJSON(TypedDict):
    lat: float
    lng: float

class ViewportJSON(TypedDict):
    northeast: LatLongCoordsJSON
    southwest: LatLongCoordsJSON

class GeometryJSON(TypedDict):
    location: LatLongCoordsJSON
    viewport: ViewportJSON


### API Return JSONs
class ResponseJSON(TypedDict):
    status: str

class PlaceResponseJSON(ResponseJSON):
    candidates: list['PlaceCandidateJSON']
class PlaceCandidateJSON(TypedDict, total=False):
    business_status: str
    formatted_address: str
    geometry: GeometryJSON
    name: str
    place_id: str

### Credentials JSON
class CredentialsJSON(TypedDict):
    API_KEY: str