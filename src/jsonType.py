from typing import Dict, Optional, TypeGuard, TypeVar, TypedDict

### Generic Classes ###
KT = TypeVar('KT'); VT = TypeVar('VT')

### Base Dictionary Class to return 'None' if key doesn't exist ###
# def is_dict(o: object) -> TypeGuard[Dict[str, object]]:
#     return isinstance(o, dict) and all(isinstance(k, str) for k in o.keys())


# # if dict
#     send vlaues through me
#     make NoneDict
# # elif iterable
#     send elements through me
# # else
#     send value out
# class NoneDict(Dict[KT, VT]):
#     def __new__(cls: type['NoneDict'], base_dict: object, *args: object, **kwargs: object) -> 'NoneDict':
#         if is_dict(base_dict):


#         return super().__new__(base_dict, *args, **kwargs)
#     def __getitem__(self, key: KT) -> Optional[VT]: # type: ignore [override]
#         print(f"#### Getting {key} from {self}")
#         return self.get(key, None)
    
    
#     def _

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


### JSON API Path Mapping Pairs

json_api_class_map: dict[ResponseJSON, str] = {
    PlaceResponseJSON:"place/findplacefromtext"
}