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

# start
traffic_server.start()