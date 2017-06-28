import asyncio
import websockets
import json
import asyncio
import threading
import datetime as dt
from dateutil import parser

## import our modules
from .database import TrafficData

class TrafficServer:

    def __init__(self, database_name: str = "Traffic", database_ip: str = None):
        """
        self.msg_queue is used to communicate with consumer_handler() and producer_handler()
        """
        self.msg_queue = asyncio.Queue()
        if not database_ip:
            self.traffic_data = TrafficData(database_name = database_name)
        else:
            self.traffic_data = TrafficData(database_name = database_name, database_ip = database_ip)
        self.loop = asyncio.get_event_loop()
        self.crawler_running = False
        self.traffic_matrix_list = []

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
            self.traffic_data.insert_analytics_traffic_pattern('[33.880079, 33.648894, -84.485086, -84.311365]')

            # time management, we want to execute script every 30 minutes
            # in order to do that we need to calculate how many seconds we should sleep
            current = dt.datetime.utcnow()
            if current.minute < 30:
                wait_seconds = 30*60 - current.minute*60 - current.second
            else:
                wait_seconds = 60*60 - current.minute*60 - current.second

            print('crawling finished')

            await asyncio.sleep(wait_seconds)
            

    def _loop_in_thread(self, loop):
        start_server = websockets.serve(self.handler, '0.0.0.0', 8765)
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_server)
        loop.create_task(self.main_crawler())
        loop.run_forever()


    def start(self):
        t = threading.Thread(target=self._loop_in_thread, args=(self.loop,))
        t.start()
        print('server served at ws://127.0.0.1:8765/')

