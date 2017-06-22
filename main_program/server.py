import asyncio
import websockets
import json
import asyncio
import threading

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
        self.crawler_frequency_second = 1800
        self.traffic_matrix_list = []

    async def consumer_handler(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                print("received", message)
                message = json.loads(message)

                # for each different message, we do different things
                if message[0] == "getHistoric":
                    geojson_object = self.traffic_data.get_historic_traffic(message[1])
                    await self.msg_queue.put(['getHistoric', geojson_object])

                elif message[0] == "getRoadData":
                    data = self.traffic_data.get_nearest_road(location_data = (message[1]['lat'], message[1]['lng']), max_dist = message[2])
                    distance = data['dist']  # did not used, maybe used later
                    road_data_id = data['doc']['id']
                    road_data_geojson = self.traffic_data.fetch_geojson_item(road_data_id)
                    await self.msg_queue.put(['getRoadData', road_data_geojson])

                elif message[0] == "getHistoricBatch":
                    data = self.traffic_data.get_historic_batch()
                    await self.msg_queue.put(['getHistoricBatch', data])

                elif message[0] == "getSelectedBatch":
                    geojson_object = self.traffic_data.get_historic_traffic(routing_info = message[1], crawled_batch_id = message[2])
                    await self.msg_queue.put(['getSelectedBatch', geojson_object])
            
            except websockets.exceptions.ConnectionClosed:
                print('a client has disconnected')
                break

    async def producer_handler(self, websocket):
        while True:
            try:
                message = await self.msg_queue.get()
                if message[0] == "getHistoric":
                    await websocket.send(json.dumps(message[1]))
                    print('sent data')

                elif message[0] == "getRoadData":
                    await websocket.send(json.dumps(message[1]))
                    print('sent data')

                elif message[0] == "getHistoricBatch":
                    await websocket.send(json.dumps(message[1]))
                    print('sent data')

                elif message[0] == "getSelectedBatch":
                    await websocket.send(json.dumps(message[1]))
                    print('sent data')
            
            except websockets.exceptions.ConnectionClosed:
                print('a client has disconnected')
                break

    async def handler(self, websocket, path):
        consumer_task = asyncio.ensure_future(self.consumer_handler(websocket))
        producer_task = asyncio.ensure_future(self.producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
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
            await asyncio.sleep(self.crawler_frequency_second)

    def _loop_in_thread(self, loop):
        start_server = websockets.serve(self.handler, 'localhost', 8765)
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_server)
        loop.create_task(self.main_crawler())
        loop.run_forever()


    def start(self):
        t = threading.Thread(target=self._loop_in_thread, args=(self.loop,))
        t.start()
        print('server served at ws://127.0.0.1:8765/')

