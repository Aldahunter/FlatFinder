from typing import Dict, Type, TypeVar, Optional

from src.jsonType import CredentialsJSON, PlaceResponseJSON, ResponseJSON

### Generic Classes ###
KT = TypeVar('KT'); VT = TypeVar('VT')
JsonType = TypeVar('JsonType')

### Base Dictionary Class to return 'None' if key doesn't exist ###
class NoneDict(Dict[KT, VT]):
    def __getitem__(self, key: KT) -> Optional[VT]: # type: ignore [override]
        return self.get(key)

### Class to securly build safe JSONs ###
class JsonBuilder:

    @staticmethod
    def build(json: dict[str, object], return_type: Type[JsonType]) -> JsonType:
        if return_type == CredentialsJSON:
            return dict(json) # type: ignore [return-value]
        else:
            return NoneDict(json) # type: ignore [return-value]
    

    class JsonTypes:
        CredentialsJSON = CredentialsJSON
        ResponseJSON = ResponseJSON
        PlaceJSON = PlaceResponseJSON