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

##
class TestTrafficServer(TrafficServer):

    async def main_crawler(self):
        """
        """
        self.crawler_running = True
        while self.crawler_running:
            print('start crawling')
            # self.traffic_data.store_matrix_json(self.traffic_matrix_list)
            # self.traffic_data.insert_analytics_traffic_pattern('[33.880079, 33.648894, -84.485086, -84.311365]')

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
traffic_server.start()
conn = traffic_server.traffic_data.conn
r.table_create('analytics_monitored_area', primary_key = 'analytics_monitored_area_id').run(conn)
r.table_create('analytics_traffic_pattern', primary_key = 'analytics_traffic_pattern_id').run(conn)
r.table('analytics_monitored_area').index_create('description').run(conn)
r.table("analytics_traffic_pattern").index_create("analytics_crawled_batch", [r.row["analytics_monitored_area_id"], r.row["crawled_batch_id"]]).run(conn)



# setup monitoring area
traffic_server.traffic_data.set_traffic_patter_monitoring_area(top=33.880079, bottom=33.648894, left=-84.485086, right=-84.311365, description='test_atlanta', grid_point_distance=1000, testing=True, force=True)
traffic_server.traffic_data.insert_analytics_traffic_pattern_between("2017-06-20T04:00:00.000Z", "2017-06-29T03:59:59.000Z", '[33.880079, 33.648894, -84.485086, -84.311365]')
