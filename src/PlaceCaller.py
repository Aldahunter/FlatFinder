from src.jsonType import PlaceCandidateJSON
from src.APIGateway import APIGateway

class PlaceCaller:

    gateway: APIGateway

    def __init__(self, gateway: APIGateway):
        self.gateway = gateway
    
    def get_place(self, place: str) -> PlaceCandidateJSON:
        return self.gateway.find_place(place)["candidates"][0]