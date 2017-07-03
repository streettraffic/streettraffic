## import system module
import json
import rethinkdb as r
import time
import datetime as dt
import asyncio
import websockets

## import custom module
from main_program.map_resource import ultil
from main_program.database import TrafficData
from main_program import tools
from main_program.server import TrafficServer

##
class TestTrafficServer(TrafficServer):

    def _loop_in_thread(self, loop):
        start_server = websockets.serve(self.handler, '0.0.0.0', 8765)
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_server)
        loop.create_task(self.main_crawler())
        loop.run_forever()


## initialize traffic server
traffic_server = TestTrafficServer(database_name= "Traffic", database_ip = "localhost")
traffic_server.start()
conn = traffic_server.traffic_data.conn
