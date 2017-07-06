## import system module
import json
import rethinkdb as r
import time

## import custom module
from main_program.map_resource import ultil
from main_program.database import TrafficData
from main_program import tools
from main_program.server import TrafficServer

## initialize traffic server
traffic_server = TrafficServer(database_name= "Traffic", database_ip = "localhost")

## atlanta tile
p1 = (33.653079, -84.505187)
p2 = (33.873635, -84.343085)
tile_matrix = ultil.get_area_tile_matrix([p1, p2], 14)
url_matrix = ultil.get_area_tile_matrix_url("traffic_json", [p1, p2], 14)

traffic_server.traffic_matrix_list = [url_matrix]

# start
traffic_server.start()