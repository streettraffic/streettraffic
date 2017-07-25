## import system module
import json
import rethinkdb as r
import time
import datetime as dt
import asyncio

## import custom module
from streettraffic.server import TrafficServer

settings = {
    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
}

## initialize traffic server
server = TrafficServer(settings)
server.start()
conn = server.traffic_data.conn
