from main_program.HERE_map import ultil

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
        total_url = base_url + str(i) + '/' + str(round(col)) + '/' + str(round(row)) + '/' + str(image_size) + '/png8?app_id=' + app_id + '&app_code=' + app_code
        print(total_url)
    
def measure_estimated_request():
    """
    measure the squares/request required to cover greenville county based on zoom level.
    since we only have 100k request available, we need to carefully arrange our request quantity.
    """
    up_left_position = (34.930522, -82.584159)
    up_right_position = (34.947532,-82.186334)
    bottom_left_position = (34.595576,-82.547509)
    for i in range(3,20):
        up_left_tile = ultil.get_tile(*up_left_position, i)
        up_right_tile = ultil.get_tile(*up_right_position, i)
        bottom_left_tile = ultil.get_tile(*bottom_left_position, i)
        square_x_length = int(up_right_tile[0]) - int(up_left_tile[0]) + 1
        square_y_length = int(up_left_tile[1]) - int(bottom_left_position[1]) + 1
        estimated_tile_in_square = square_x_length * square_y_length
        print(i, estimated_tile_in_square)


#get_traffic_tile_of_different_zoom()
measure_estimated_request()