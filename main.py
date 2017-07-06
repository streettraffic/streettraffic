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
info = ultil.get_area_tile_matrix([cor1, cor2], 14)
matrix1 = ultil.get_area_tile_matrix_url("traffic_json", [cor1, cor2], 14)
#matrix1 = ultil.get_area_tile_matrix_url("map_tile", cor1, cor2, 14)
#img_matrix = ultil.assemble_matrix_images(matrix1)


## Dr. Allen house
#cor1 = (34.939348, -82.456024)
#cor2 = (34.910812, -82.420834)
#matrix = ultil.get_area_tile_matrix_url(cor1, cor2, 14)
#img_matrix = ultil.assemble_matrix_images(matrix)


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

with open('traffic data samples/google_routing.json') as f:
    data = json.load(f)
    
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
matrix2 = ultil.get_area_tile_matrix_url("traffic_json", [man_point1, man_point2], 14)

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
tile_matrix = ultil.get_area_tile_matrix([p1, p2], 14)
url_matrix = ultil.get_area_tile_matrix_url("traffic_json", [p1, p2], 14)

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
#traffic_server.traffic_data.get_analytics_traffic_pattern_between(start_time_iso,end_time_iso, '[33.880079, 33.648894, -84.485086, -84.311365]')

## little benchmark
#query = r.table('flow_item').get_field('flow_item_id').limit(10000).run(conn)
#flow_item_id_collection = []
#crawled_batch_id = '0e8e60c5-3936-41f0-86fc-3b6e0e37ac4a'
#for item in query:
#    flow_item_id_collection += [item]
#    
#def batch_query_get_all(flow_item_id_collection, crawled_batch_id):
#    batch = []
#    for flow_item_id in flow_item_id_collection:
#        batch += [[flow_item_id, crawled_batch_id]]
#    return batch

### first way, use a for loop
#start_time = time.time()
#for flow_item_id in flow_item_id_collection:
#    r.table('flow_data').get_all([flow_item_id, crawled_batch_id], index='flow_crawled_batch').run(conn)
#
#print('first way used', time.time() - start_time, 'seconds')
#    
### second way, use batch
#start_time = time.time()
#r.table('flow_data').get_all(*batch_query_get_all(flow_item_id_collection, crawled_batch_id), index='flow_crawled_batch').run(conn)
#print('second way used', time.time() - start_time, 'seconds')
#    

#p1 = (38.718152,-77.374552)
#p2 = (39.465786, -76.455926)
#tile_matrix = ultil.get_area_tile_matrix(p1, p2, 14)
    
# Miami
cor1 = (25.803018, -80.267741)
cor2 = (25.726957, -80.192897)
info = ultil.get_area_tile_matrix([cor1, cor2], 14)
matrix = ultil.get_area_tile_matrix_url("map_tile", [cor1, cor2], 14)

# Use polygon to get area_tile
polygon_points = [[25.890099,-80.264561], [25.851873,-80.308744], [25.811230,-80.248538], [25.848596,-80.215765]]
polygon = ultil.produce_polygon(polygon_points, 14)
info = ultil.get_area_tile_matrix(polygon_points, 14, True)
atlanta_polygon = [[33.73233462866422, -84.43645477294922],
 [33.786566509489155, -84.37259674072266],
 [33.7597402884442, -84.34444427490234],
 [33.7094898901883, -84.41619873046875],
 [33.73233462866422, -84.43645477294922]]

new_york_polygon = [[40.7701418259051, -74.15771484375],
 [40.76806170936613, -73.8720703125],
 [40.88444793903562, -73.27056884765625],
 [40.959159772134896, -72.6800537109375],
 [40.824201998489904, -72.61688232421875],
 [40.54093880017256, -74.410400390625],
 [40.7701418259051, -74.15771484375]]

#info = ultil.get_area_tile_matrix(atlanta_polygon, 14, True)
#matrix = ultil.get_area_tile_matrix_url("map_tile", atlanta_polygon, 14, True)
##img_matrix = ultil.assemble_matrix_images(matrix)


washington_baltimore_polygon = [[38.77978137804918, -77.200927734375],
 [38.77549900381297, -76.9482421875],
 [38.86965182408357, -76.7999267578125],
 [39.002110299225144, -76.7999267578125],
 [39.06184913429154, -76.783447265625],
 [39.16414104768743, -76.5692138671875],
 [39.22799807055236, -76.4208984375],
 [39.33854604847979, -76.4044189453125],
 [39.457402514270825, -76.5142822265625],
 [39.436192999314095, -76.70654296875],
 [39.32579941789297, -76.8768310546875],
 [39.198205348894795, -76.8878173828125],
 [39.01918369029135, -77.05810546875],
 [39.06184913429154, -77.1624755859375],
 [38.950865400919994, -77.2613525390625],
 [38.8225909761771, -77.2503662109375],
 [38.77978137804918, -77.200927734375]]

washington_baltimore_info = ultil.get_area_tile_matrix(washington_baltimore_polygon, 14, True)
washington_baltimore_matrix = ultil.get_area_tile_matrix_url("map_tile", washington_baltimore_polygon, 14, True)
#img_matrix = ultil.assemble_matrix_images(matrix)

def matrix_coverage(matrix):
    filled_count = 0
    None_count = 0
    for row in range(len(matrix)):
        for col in range(len(matrix.iloc[0])):
            if matrix.iloc[row, col]:
                filled_count += 1
            else:
                None_count += 1
    
    print('matrix has a total of', len(matrix) *len(matrix.iloc[0]), 'tiles')
    print(filled_count, 'of them are filled')
    print(None_count, 'of them are None because of the polygon limitation')
                

newyork_boston_polygon = [[40.51066695034288, -74.168701171875],
 [40.606654663050485, -74.04098510742188],
 [40.57015381856105, -73.92974853515625],
 [40.834593138080244, -72.55096435546875],
 [41.000629848685385, -72.59490966796875],
 [40.83043687764923, -73.7786865234375],
 [41.033787135218645, -73.50128173828125],
 [41.269549502842565, -72.8009033203125],
 [41.269549502842565, -72.2845458984375],
 [41.376808565702355, -71.4495849609375],
 [41.7180304600481, -71.3671875],
 [41.475660200278206, -71.1309814453125],
 [41.86137915587359, -70.5377197265625],
 [41.94314874732696, -70.5377197265625],
 [41.97991089691236, -70.6695556640625],
 [42.14304156290942, -70.6475830078125],
 [42.26917949243505, -70.8453369140625],
 [42.248851700720955, -70.960693359375],
 [42.335199554872325, -71.03759765625],
 [42.51260171573666, -70.8343505859375],
 [42.64204079304425, -70.59814453125],
 [42.66628070564928, -70.872802734375],
 [42.69454866207692, -71.2628173828125],
 [42.4923525914282, -71.575927734375],
 [42.19189902447192, -72.059326171875],
 [41.50446357504803, -73.49853515625],
 [41.469486382476376, -74.07257080078125],
 [41.05243077390835, -74.31976318359375],
 [40.56389453066509, -74.34722900390625],
 [40.51066695034288, -74.168701171875]]
newyork_boston_info = ultil.get_area_tile_matrix(newyork_boston_polygon, 14, True)
newyork_boston_matrix = ultil.get_area_tile_matrix_url("map_tile", newyork_boston_polygon, 14, True)
