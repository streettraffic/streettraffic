from streettraffic.server import TrafficServer
from streettraffic.predefined.cities import San_Francisco_polygon

settings = {
    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',  # this is where you put your App ID from here.com
    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw', # this is where you put your App Code from here.com
    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
}


## initialize traffic server
server = TrafficServer(settings)
server.start()