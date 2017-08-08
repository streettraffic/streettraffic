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
server = TrafficServer(settings, database_ip='costahuang.me')
server.start()
conn = server.traffic_data.conn

with open('area_collection.json') as f:
    polygon_collection = json.load(f)


# setup monitoring area
#for polygon_item in polygon_collection:
#    server.traffic_data.set_traffic_patter_monitoring_area(polygon_item[1], description=polygon_item[0], grid_point_distance=1000, testing=True, force=True)


date = ["2017-08-03T04:00:00.000Z","2017-08-05T03:00:00.000Z"]
for polygon in polygon_collection:
    try:
        server.traffic_data.set_traffic_patter_monitoring_area(polygon['polygon'],
            description=polygon['area_description'],
            grid_point_distance=1000,
            testing=True)
    except Exception as e:
        print(e)
    analytics_monitored_area_id = r.table('analytics_monitored_area') \
        .get_all(polygon['area_description'], index="description") \
        .get_field('analytics_monitored_area_id') \
        .run(conn).next()
    server.traffic_data.insert_analytics_traffic_pattern_between(date[0], date[1], analytics_monitored_area_id)
    