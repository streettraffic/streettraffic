import rethinkdb as r

## import custom module
from streettraffic.server import TrafficServer
from streettraffic.predefined.cities import San_Francisco_polygon

settings = {
    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
}


## initialize traffic server
server = TrafficServer(settings)
San_Francisco_matrix = server.util.get_area_tile_matrix_url("traffic_json", San_Francisco_polygon, 14, True)
server.start()
conn = server.traffic_data.conn

# City Polygon
Atlanta_downtown = [[33.74775138989557, -84.4464111328125], [33.77144211983988, -84.36058044433594], [33.72548184547877, -84.34684753417969], [33.706062655101206, -84.39800262451172], [33.74775138989557, -84.4464111328125]]

# ISO formatted time string
date_start = "2017-07-4T04:00:00.000Z"
date_end = "2017-07-6T03:00:00.000Z"

# setup monitoring area
server.traffic_data.set_traffic_patter_monitoring_area(Atlanta_polygon, description='Atlanta_downtown', grid_point_distance=1000, force=True)
analytics_monitored_area_id = r.table('analytics_monitored_area').get_all('Atlanta_downtown', index="description").get_field('analytics_monitored_area_id').run(conn).next()

# insert traffic pattern between date
server.traffic_data.insert_analytics_traffic_pattern_between(date_start, date_end, analytics_monitored_area_id)
