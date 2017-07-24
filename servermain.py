## import system module
import json
import rethinkdb as r
import time
import datetime as dt
import asyncio

## import custom module
from streettraffic.map_resource.utility import Utility
from streettraffic.database import TrafficData
from streettraffic import tools
from streettraffic.server import TrafficServer


## initialize traffic server
traffic_server = TrafficServer(database_name="Traffic", database_ip="localhost")
traffic_server.start()
conn = traffic_server.traffic_data.conn
