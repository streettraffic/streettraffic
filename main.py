from main_program.map_resource import ultil
from main_program.database import TrafficData
from main_program import tools
from main_program.server import TrafficServer
from main_program.datafeed import DataFeed
import json
import rethinkdb as r
import time
import datetime
from dateutil import parser


## Furman's coordinates is 34.9237° N, 82.4383° W
## which translate to 34.9237°, -82.4383° according to 
## https://msdn.microsoft.com/en-us/library/aa578799.aspx


zoom = 14
(col, row) = ultil.get_tile(34.9237, -82.4383, zoom)
print('furman zoom/col/row is %d/%d/%d' % (zoom,round(col),round(row)))
## get traffic tile
#
# id4 https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4440/6494/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw
# id2 https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4440/6493/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw
# id3 https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4439/6494/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw
# id1 https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4439/6493/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw
#
## download those pictures and edit them together in the following format
#
#############
#     #     #
# id1 # id2 #
#     #     #
#############
#     #     #
# id3 # id4 #
#     #     #
############# 

(col, row) = (4440, 6493)
## get flow tile (transparent traffic map)
#
# https://1.traffic.maps.cit.api.here.com/maptile/2.1/flowtile/newest/normal.day/14/4440/6493/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw

quadkey = ultil.get_quadkeys(4440, 6493, zoom)
## get the same traffic tile by using quadkey
#
# https://tiles.traffic.cit.api.here.com/traffic/6.0/tiles/quadkeytraffic?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&depth=8bit
#
## get the traffic info (json) by using same quadkey/location
#
# https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&depth=8bit

def get_traffic_tile_of_different_zoom():
    """
    get traffic tile of different zoom
    """
    base_url = 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/'
    app_id = 'F8aPRXcW3MmyUvQ8Z3J9'
    app_code = 'IVp1_zoGHdLdz0GvD_Eqsw'
    image_size = 512  # or could choose 512
    for i in range(20):
        (col, row) = ultil.get_tile(34.8529419802915, -82.3969868197085, i)  # coffee underground lat and lon
        total_url = base_url + str(i) + '/' + str(int(col)) + '/' + str(int(row)) + '/' + str(image_size) + '/png8?app_id=' + app_id + '&app_code=' + app_code
        print(total_url)
    
def measure_estimated_request():
    """
    measure the squares/request required to cover greenville county based on zoom level.
    since we only have 100k request available, we need to carefully arrange our request quantity.
    """
    up_right_position = (34.947532,-82.186334)
    bottom_left_position = (34.595576,-82.547509)
    for i in range(3,20):
        up_right_tile = ultil.get_tile(*up_right_position, i)
        bottom_left_tile = ultil.get_tile(*bottom_left_position, i)
        square_x_length = abs(int(up_right_tile[0]) - int(bottom_left_tile[0])) + 1
        square_y_length = abs(int(up_right_tile[1]) - int(bottom_left_tile[1])) + 1
        #print('x',square_x_length, 'y',square_y_length)
        estimated_tile_in_square = square_x_length * square_y_length
        print(i, estimated_tile_in_square)


#get_traffic_tile_of_different_zoom()
#measure_estimated_request()

## atlanta worst traffic point:
altanta_worst = (33.670156, -84.325984)
altanta_worst_map_tile = ultil.get_map_tile_resource(altanta_worst, "latlon", 14, 512)
atlanta_worst_json_tile = ultil.get_traffic_json_resource(altanta_worst, "latlon", 14)

## atlanta tile
cor1 = (33.728999, -84.395856)#(33.766764, -84.409533)
cor2 = (33.775902, -84.363917)#(33.740003, -84.368978)
info = ultil.get_area_tile_matrix(cor1, cor2, 14)
matrix1 = ultil.get_area_tile_matrix_url("traffic_json", cor1, cor2, 14)
#matrix1 = ultil.get_area_tile_matrix_url("map_tile", cor1, cor2, 14)
#img_matrix = ultil.assemble_matrix_images(matrix1)


## Dr'allen house
#cor1 = (34.939348, -82.456024)
#cor2 = (34.910812, -82.420834)
#matrix = ultil.get_area_tile_matrix_url(cor1, cor2, 14)
#img_matrix = ultil.assemble_matrix_images(matrix)

# Miami
#cor1 = (25.803018, -80.267741)
#cor2 = (25.726957, -80.192897)
#matrix = ultil.get_area_tile_matrix_url(cor1, cor2, 14)

#with open('test.json') as f:
#    data = json.load(f)

traffic_server = TrafficServer(database_name= "Traffic", database_ip = "localhost")
traffic_server.start()
conn = traffic_server.traffic_data.conn

#r.set_loop_type("asyncio")
#data_feed = DataFeed('test')

## Nice to know that we have set up datatime object correctly
# r.db('Traffic').table('flow_data').between(r.expr(yourdate), r.epoch_time(int(time.time())), index='created_timestamp').run()

#json_data = traffic_data.read_traffic_data('https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&responseattributes=sh,fc')
#
#traffic_data.insert_json_data(json_data)

## inserting test data into test.geo table
#current_epoch = 1497446043
#
#for i in range(10):
#    data = []
#    for i in range(10):
#        data += [{'timestamp': r.epoch_time(time.time()) }]
#        
#    r.table('geo').insert(data).run()
#    time.sleep(1)
#        
#print('finished')

#test_geojson1 = traffic_data.fetch_geojson_item('0ccbbac6-12b8-4681-a1a4-9e15e89bd4e1')
#test_geojson2 = traffic_data.fetch_geojson_item('08901fc1-b9d3-4c3a-a48e-6be807df39dc')
#test_data = TrafficData.generate_geojson_collection([test_geojson1,test_geojson2 ])

## display traffic test
#display_traffic = traffic_data.display_json_traffic(['974f1914-8179-4518-8f26-6b013b998d72'])

## atlanta traffic original documents id
atlanta_traffic_original_doc_ids = [
    '4f159114-e1d9-4d21-881d-16c3f199b381',
    '38070cae-aa79-4828-a95f-31df91883846',
    'ade4f658-8760-449e-8747-3c306588fd47',
    'a805261f-341d-4790-90d2-8a5d6d88ca37',
    '1ae29972-6c2d-4145-9226-a9c34a8498c4',
    'fb39a2cf-d7e7-49bf-a7bd-b0e713539447',
    '9a136e28-67a8-4d3e-beda-351c82565c7f',
    '9a136e28-67a8-4d3e-beda-351c82565c7f',
    'a3f3dc2b-eea0-40d0-87c2-7ad7b8cc0fdd',
]


## given a point, we want to know the closest road to it
#test_start_location = (33.736818, -84.394652)
#test_end_location = (33.769922, -84.377616)

#with open('traffic data samples/google_routing.json') as f:
#    data = json.load(f)
    
## testing geospatial query
#t1 = {"lat":33.74416482021835,"lng":-84.39327120780945}
#t2 = {"lat":33.74251436232895,"lng":-84.39330339431763}
#query_point = {"lat":33.743370820116844,"lng":-84.39433336257935}
#t3 = {"lat":33.74143931727222,"lng":-84.3949556350708}
#t4 = {"lat":33.74416035956415,"lng":-84.39240217208862}

#r.table('geo_test').insert([
#  {
#    id: 1,
#    name: 't1',
#    location: r.point(-84.39327120780945,33.74416482021835)
#  },
#  {
#    id: 2,
#    name: 't2',
#    location: r.point(-84.39330339431763,33.74251436232895)
#  },
#  {
#    id: 3,
#    name: 'line',
#    location: r.line([-84.39327120780945,33.74416482021835], [-84.39330339431763,33.74251436232895])
#  }
#])
    
    
## Manhattan island
man_point1 = (40.710943, -74.017559)
man_point2 = (40.728209, -73.982583)
matrix2 = ultil.get_area_tile_matrix_url("traffic_json", man_point1, man_point2, 14)

#traffic_server.traffic_data.store_matrix_json([matrix1, matrix2])
# .get_all(crawled_batch_id, index = "crawled_batch_id")

#flow_data_feed = r.db('test').table('flow_data').changes().run(traffic_server.traffic_data.conn)
#road_data_feed = r.db('test').table('road_data').changes().run(traffic_server.traffic_data.conn)
#original_data_feed = r.db('test').table('original_data').changes().run(traffic_server.traffic_data.conn)
#crawled_batch_feed = r.db('test').table('crawled_batch').changes().run(traffic_server.traffic_data.conn)

#for original_data_id in record[0]:
#    r.db('test').table('original_data').get(original_data_id).delete().run(traffic_server.traffic_data.conn)
#for flow_data_id in record[1]:
#    r.db('test').table('flow_data').get(flow_data_id).delete().run(traffic_server.traffic_data.conn)
#for road_data_id in record[2]:
#    r.db('test').table('road_data').get(road_data_id).delete().run(traffic_server.traffic_data.conn)



# r.net.connection_type = r.net.DefaultConnection


## Crawl atlanta city
p1 = (33.653079, -84.505187)
p2 = (33.873635, -84.343085)
tile_matrix = ultil.get_area_tile_matrix(p1, p2, 14)
url_matrix = ultil.get_area_tile_matrix_url("traffic_json", p1, p2, 14)

##
#now = time.time()
#flow_data = r.table('flow_data').get('{"DE": "10th St/Exit 250", "LE": 0.55387, "PC": 4132, "QD": "+"}').run(traffic_server.traffic_data.conn)
#print(time.time() - now)
#
#now = time.time()
#flow_data = r.table('flow_data').get('{"DE": "10th St/Exit 250", "LE": 0.55387, "PC": 4132, "QD": "+"}')['CF']['0358a775-569b-464f-abd7-25ab1da6e985'].run(traffic_server.traffic_data.conn)
#print(time.time() - now)


## Spatial sampling for atlanta area
sampling_points_atlanta = traffic_server.traffic_data.spatial_sampling_points(top=33.880079, bottom=33.648894, left=-84.485086, right=-84.311365, grid_point_distance = 1000)
sampling_points_atlanta_plot = traffic_server.traffic_data.format_list_points_for_display(sampling_points_atlanta)
#x = traffic_server.traffic_data.set_traffic_patter_monitoring_area(top=33.880079, bottom=33.648894, left=-84.485086, right=-84.311365, description='test_atlanta', grid_point_distance=1000, testing=True, force=True)

# analyzing traffic patter
start = datetime.datetime(2017,6,27,0,0,0, tzinfo = r.make_timezone('00:00'))
end = datetime.datetime(2017,6,27,23,0,0, tzinfo = r.make_timezone('00:00'))
analytics_monitored_area_id = '[33.880079, 33.648894, -84.485086, -84.311365]'
start_time_iso = "2017-06-23T04:00:00.000Z"
end_time_iso = "2017-06-24T03:59:59.000Z"
#traffic_server.traffic_data.update_analytics_traffic_pattern("2017-06-23T04:00:00.000Z","2017-06-24T03:59:59.000Z",'[33.880079, 33.648894, -84.485086, -84.311365]')