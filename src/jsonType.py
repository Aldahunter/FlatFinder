from typing import TypedDict, Union

### API Return JSONs
class ResponseJSON(TypedDict):
    status: str

class PlaceJSON(ResponseJSON):
        candidates: list['_PlaceCandidates']
class _PlaceCandidates(TypedDict, total=False):
    formatted_address: str
    geometry: 'Geometry'
    name: str
    place_id: str
class LatLongCoords(TypedDict):
    lat: float
    lng: float
class Viewport(TypedDict):
    northeast: LatLongCoords
    southwest: LatLongCoords
class Geometry(TypedDict):
    location: LatLongCoords
    viewport: Viewport


class DistanceMatrixJSON(ResponseJSON):
        destination_addresses: list[str]
        origin_addresses: list[str]
        rows: list['_DistanceMatrixRow']
class _DistanceMatrixRow(TypedDict, total=False):
    elements: list['_DistanceMatrixElement']
class _DistanceMatrixElement(TypedDict, total=False):
    distance: '_TextValueObject'
    duration: '_TextValueObject'
    status: str
class _TextValueObject(TypedDict):
    text: str
    value: int

### Credentials JSON
class CredentialsJSON(TypedDict):
    API_KEY: str
