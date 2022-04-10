from src.api.jsonType import PlaceCandidateJSON
from src.database.DBTables import Geometry, LatLongCoords, Place, Viewport

class JsonToDbParser:

    @staticmethod
    def build_place_entry(place_json: PlaceCandidateJSON) -> Place:
        return Place(
            place_id = place_json['place_id'],
            name = place_json['name'],
            formatted_address = place_json.get('formatted_address'),
            business_status = place_json.get('business_status'),
            geometry = Geometry(
                    location = LatLongCoords(
                            lat = place_json.get('geometry', {}).get('location', {}).get('lat'),
                            lng = place_json.get('geometry', {}).get('location', {}).get('lng')),
                    viewport = Viewport(
                        northeast = LatLongCoords(
                            lat = place_json.get('geometry', {}).get('viewport', {}).get('northeast', {}).get('lat'),
                            lng = place_json.get('geometry', {}).get('viewport', {}).get('northeast', {}).get('lng')
                        ),
                        southwest = LatLongCoords(
                            lat = place_json.get('geometry', {}).get('viewport', {}).get('southwest', {}).get('lat'),
                            lng = place_json.get('geometry', {}).get('viewport', {}).get('southwest', {}).get('lng')
                        ))))


    ### Get DBTable columns, see which are foreign keys
    ### Get JSON keys, see which are other JSONs
    ### Align columns with keys
    ### Create Table Entries filled with JSON values (lowest rungs first)