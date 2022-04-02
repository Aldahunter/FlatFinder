from src.DBShield import DBShield
from src.jsonType import Geometry, LatLongCoords, PlaceCandidate, PlaceJSON, Viewport
from .APIGateway import APIGateway
from os.path import dirname, join as pathJoin


class GetStations:

    def __init__(self, stations_file: str):
        try:
            with open(stations_file) as f:
                lines: list[str] = [line.strip() for line in f.readlines() if line.strip()]
        except IOError as err:
            err.strerror = "The Station Names file is not accessible"
            raise err
            
        
        stations: list[str] = []
        station_suffix: str = ''
        for line in lines:
            
            if line.startswith('#'):
                station_suffix = line.replace('#', '').strip()
            else:
                stations.append(' '.join([line, station_suffix]))

        gw: APIGateway = APIGateway(pathJoin(dirname(__file__), '..', "credentials.json"))
        station: str = stations[0]
        print(f"Searching for '{station}'.")

        placeJson: PlaceJSON = gw.find_place(station)
        print(placeJson)

        ### Step 1 - Align Data ###
        placeC: PlaceCandidate = placeJson['candidates'][0]
        place_kwargs = {'place_id': placeC['place_id'],
                        'name': placeC['name'],
                        'formatted_address': placeC['formatted_address'],
                        'business_status': placeC['business_status'],
                        'geometry_id': None}
        
        gm: Geometry = placeC['geometry']
        geom_kwargs = {'location_id': None,
                       'viewport_id': None}
        
        lc: LatLongCoords = gm['location']
        loct_kwargs = {'lat': lc['lat'],
                       'long': lc['lng']}

        vp: Viewport = gm['viewport']
        vwpt_kwargs =  {'northeast_id': None,
                        'southwest_id': None}

        vp_ne: LatLongCoords = vp['northeast']
        vpne_kwargs = {'lat': vp_ne['lat'],
                       'long': vp_ne['lng']}

        vp_sw: LatLongCoords = vp['southwest']
        vpsw_kwargs = {'lat': vp_sw['lat'],
                       'long': vp_sw['lng']}

        ### Step 2 - Start up DB ###

        db = DBShield('DOESNT MAKE A DIFFERENCE WHAT I PUT HERE YET')

        ### Step 2 - Fill data into tables ###
        
        viewport_ne = db.tables.LatLongCoords(**vpne_kwargs)
        viewport_sw = db.tables.LatLongCoords(**vpsw_kwargs)

        db.session.add_all([viewport_ne, viewport_sw])
        db.session.commit()
        vwpt_kwargs['northeast_id'] = viewport_ne.id
        vwpt_kwargs['southwest_id'] = viewport_sw.id

        viewport = db.tables.Viewport(**vwpt_kwargs)
        location = db.tables.LatLongCoords(**loct_kwargs)

        db.session.add_all([viewport, location])
        db.session.commit()
        geom_kwargs['location_id'] = location.id
        geom_kwargs['viewport_id'] = viewport.id

        geometry = db.tables.Geometry(**geom_kwargs)

        db.session.add(geometry)
        db.session.commit()
        place_kwargs['geometry_id'] = geometry.id

        place = db.tables.Place(**place_kwargs)

        db.session.add(place)
        db.session.commit()
        






if __name__ == '__main__':
    file_path: str = pathJoin(dirname(__file__),'..','resources', 'ListOfStations.txt')
    GetStations(file_path)
