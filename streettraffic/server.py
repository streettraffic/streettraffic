import asyncio
import websockets
import json
import asyncio
import threading
import datetime as dt
from dateutil import parser
import http.server
import socketserver
import os
from typing import Dict, List
import urllib
import posixpath

## import our modules
from .database import TrafficData
from .map_resource.utility import Utility

class TrafficServer:

    def __init__(self, settings: Dict, database_name: str = "Traffic", database_ip: str = None):
        """
        self.msg_queue is used to communicate with consumer_handler() and producer_handler()
        """
        self.msg_queue = asyncio.Queue()
        if not database_ip:
            self.traffic_data = TrafficData(database_name=database_name, database_ip='localhost')
        else:
            self.traffic_data = TrafficData(database_name=database_name, database_ip=database_ip)
        self.util = Utility(settings)
        self.loop = asyncio.get_event_loop()
        self.crawler_running = False
        self.traffic_matrix_list = []
        self.traffic_pattern_list = []
        self.http_port = 9000

    def init_http_server(self):
        Handler = NonRootHTTPRequestHandler
        httpd = socketserver.TCPServer(("", self.http_port), Handler)
        httpd.serve_forever()
    
    async def consumer_handler(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                # print("received", message)
                message = json.loads(message)

                # for each different message, we do different things
                if message[0] == "getHistoric":
                    geojson_object = self.traffic_data.get_historic_traffic(message[1])
                    # await self.msg_queue.put(['getHistoric', geojson_object])
                    await websocket.send(json.dumps(geojson_object))
                    print('sent data')

                elif message[0] == "getRoadData":
                    data = self.traffic_data.get_nearest_road(location_data = (message[1]['lat'], message[1]['lng']), max_dist = message[2])
                    distance = data['dist']  # did not used, maybe used later
                    road_data_id = data['doc']['road_data_id']
                    road_data_geojson = self.traffic_data.fetch_geojson_item(road_data_id)
                    # await self.msg_queue.put(['getRoadData', road_data_geojson])
                    await websocket.send(json.dumps(road_data_geojson))
                    print('sent data')

                elif message[0] == "getHistoricBatch":
                    data = self.traffic_data.get_historic_batch()
                    # await self.msg_queue.put(['getHistoricBatch', data])
                    await websocket.send(json.dumps(data))
                    print('sent data')

                elif message[0] == "getSelectedBatch":
                    geojson_object = self.traffic_data.get_historic_traffic(routing_info = message[1], crawled_batch_id = message[2])
                    # await self.msg_queue.put(['getSelectedBatch', geojson_object])
                    await websocket.send(json.dumps(geojson_object))
                    print('sent data')

                elif message[0] == "getSelectedBatchList":
                    multipe_geojson_objects = []
                    for crawled_batch_item in message[2]:
                        multipe_geojson_objects += [{
                            "crawled_batch_id": crawled_batch_item['crawled_batch_id'],
                            "crawled_batch_id_traffic": self.traffic_data.get_historic_traffic(routing_info = message[1], crawled_batch_id = crawled_batch_item['crawled_batch_id']),
                            "crawled_timestamp": crawled_batch_item['crawled_timestamp']
                        }]

                    ## sort based on timestamp
                    multipe_geojson_objects.sort(key = lambda item: parser.parse(item['crawled_timestamp']))
                    for item in multipe_geojson_objects:
                        print(item['crawled_timestamp'])
                    await websocket.send(json.dumps(multipe_geojson_objects))
                    print('sent data')

                elif message[0] == "getTrafficPattern":
                    print(message)
                    traffic_pattern = self.traffic_data.get_analytics_traffic_pattern_between(message[1], message[2], analytics_monitored_area_description = message[3])
                    await websocket.send(json.dumps(traffic_pattern))
                    print('sent data')

                elif message[0] == "getRouteTraffic":
                    print("getRouteTraffic")
                    route_traffic = self.traffic_data.get_historic_traffic_between(message[1], message[2], message[3])
                    await websocket.send(json.dumps(route_traffic))
                    print('sent data')

                elif message[0] == "getMultipleDaysRouteTraffic":
                    print("getMultipleDaysRouteTraffic")
                    route_traffic = self.traffic_data.get_historic_traffic_multiple_days(message[1], message[2])
                    await websocket.send(json.dumps(route_traffic))
                    print('sent data')

                elif message[0] == "getAnalyticsMonitoredAreaDescriptionCollection":
                    print("getAnalyticsMonitoredAreaDescriptionCollection")
                    analytics_monitored_area_description_collection = self.traffic_data.get_analytics_monitored_area_description_collection()
                    await websocket.send(json.dumps(analytics_monitored_area_description_collection))
                    print('sent data')
            
            except websockets.exceptions.ConnectionClosed:
                print('a client has disconnected')
                break


    async def handler(self, websocket, path):
        consumer_task = asyncio.ensure_future(self.consumer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        print('finished')

    async def main_crawler(self):
        """
        """
        self.crawler_running = True
        while self.crawler_running:
            print('start crawling')
            self.traffic_data.store_matrix_json(self.traffic_matrix_list)
            for traffic_pattern in self.traffic_pattern_list:
                self.traffic_data.insert_analytics_traffic_pattern(traffic_pattern)

            # time management, we want to execute script every 30 minutes
            # in order to do that we need to calculate how many seconds we should sleep
            current = dt.datetime.utcnow()
            if current.minute < 30:
                wait_seconds = 30*60 - current.minute*60 - current.second
            else:
                wait_seconds = 60*60 - current.minute*60 - current.second

            print('crawling finished')

            await asyncio.sleep(wait_seconds)
            

    def _loop_in_thread(self):
        start_server = websockets.serve(self.handler, '0.0.0.0', 8765)
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()


    def start(self):
        t1 = threading.Thread(target=self._loop_in_thread)
        t1.start()
        t2 = threading.Thread(target=self.init_http_server)
        t2.start()
        print('websocket served at ws://127.0.0.1:8765')
        print("Web UI served at  http://127.0.0.1:" + str(self.http_port))
        print('to run the crawler, call server.run_crawler()')

    def run_crawler(self):
        self.loop.call_soon_threadsafe(self.loop.create_task, self.main_crawler())


class NonRootHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    """This class is used to host website in the ``webui`` folder.
    Notice SimpleHTTPRequestHandler only host the files in the 
    current folder

    """

    def translate_path(self, path):
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        ## my code to override:
        web_dir = os.path.join(os.path.dirname(__file__), 'webui')
        path = web_dir
        ## my code to override ends.
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path