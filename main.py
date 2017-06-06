from main_program.HERE_map import ultil

## Furman's coordinates is 34.9237° N, 82.4383° W
## which translate to 34.9237°, -82.4383° according to 
## https://msdn.microsoft.com/en-us/library/aa578799.aspx

zoom = 14
(col, row) = get_tile(34.9237, -82.4383, zoom)
print('furman zoom/col/row is %d/%d/%d' % (zoom,col,row))

# id4 https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4440/6494/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw
# id2 https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4440/6493/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw
# id3 https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4439/6494/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw
# id1 https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4439/6493/256/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw
#
# download those pictures and edit them together in the following format
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