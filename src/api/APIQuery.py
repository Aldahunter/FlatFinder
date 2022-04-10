from typing import Optional

class APIQuery(dict[str, str]):

    def __init__(self, **kwargs: str) -> None:
        super().__init__(**kwargs)

    def add_key(self, api_key: Optional[str]) -> None:
        if (self.get("key", None) is None) and (api_key is not None):
            self['key'] = api_key

    def add_location_bias(self, location_bias: Optional[str]) -> None:
        if (self.get("locationbias", None) is None) and (location_bias is not None):
            self['key'] = location_bias