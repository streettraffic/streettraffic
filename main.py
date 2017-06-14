from main_program.map_resource import ultil
from main_program.database import TrafficData
from main_program import tools
import json
import rethinkdb as r
import time


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
cor1 = (33.766764, -84.409533)
cor2 = (33.740003, -84.368978)
info = ultil.get_area_tile_matrix(cor1, cor2, 14)
matrix = ultil.get_area_tile_matrix_url("traffic_json", cor1, cor2, 14)
#img_matrix = ultil.assemble_matrix_images(matrix)


## Dr'allen house
#cor1 = (34.939348, -82.456024)
#cor2 = (34.910812, -82.420834)
#matrix = ultil.get_area_tile_matrix_url(cor1, cor2, 14)
#img_matrix = ultil.assemble_matrix_images(matrix)

# Miami
#cor1 = (25.803018, -80.267741)
#cor2 = (25.726957, -80.192897)
#matrix = ultil.get_area_tile_matrix_url(cor1, cor2, 14)

with open('test.json') as f:
    data = json.load(f)

traffic_data = TrafficData()

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