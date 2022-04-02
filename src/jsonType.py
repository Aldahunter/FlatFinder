from typing import TypedDict

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

class PlaceJSON(ResponseJSON):
    candidates: list['PlaceCandidate']
class PlaceCandidate(TypedDict, total=False):
    business_status: str
    formatted_address: str
    geometry: Geometry
    name: str
    place_id: str

### Credentials JSON
class CredentialsJSON(TypedDict):
    API_KEY: str
