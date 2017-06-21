## import system module
import json
import rethinkdb as r
import time

## import custom module
from .map_resource import ultil
from .database import TrafficData
from . import tools
from .server import TrafficServer

## initialize traffic server
traffic_server = TrafficServer()

## start assemble data

## atlanta tile
cor1 = (33.766764, -84.409533)
cor2 = (33.740003, -84.368978)
matrix1 = ultil.get_area_tile_matrix_url("traffic_json", cor1, cor2, 14)

## Manhattan island
man_point1 = (40.710943, -74.017559)
man_point2 = (40.728209, -73.982583)
matrix2 = ultil.get_area_tile_matrix_url("traffic_json", man_point1, man_point2, 14)

traffic_server.traffic_matrix_list = [matrix1, matrix2]

# start
traffic_server.start()