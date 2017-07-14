## import system module
import json
import rethinkdb as r
import time
import datetime as dt
import asyncio

## import custom module
from main_program.map_resource import ultil
from main_program.database import TrafficData
from main_program import tools
from main_program.server import TrafficServer

class TestTrafficServer(TrafficServer):

    async def main_crawler(self):
        """
        """
        self.crawler_running = True
        while self.crawler_running:
            print('start crawling')
            self.traffic_data.store_matrix_json(self.traffic_matrix_list)
            #self.traffic_data.insert_analytics_traffic_pattern('[33.880079, 33.648894, -84.485086, -84.311365]')

            # time management, we want to execute script every 30 minutes
            # in order to do that we need to calculate how many seconds we should sleep
            current = dt.datetime.utcnow()
            if current.minute < 30:
                wait_seconds = 30*60 - current.minute*60 - current.second
            else:
                wait_seconds = 60*60 - current.minute*60 - current.second

            print('crawling finished')

            await asyncio.sleep(wait_seconds)    


## initialize traffic server
traffic_server = TestTrafficServer(database_name= "Traffic", database_ip = "localhost")

# start
traffic_server.start()