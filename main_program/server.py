import asyncio
import websockets
import json
import asyncio
import threading

## import our modules
from .database import TrafficData

class TrafficServer:

    def __init__(self):
        self.msg_queue = asyncio.Queue()
        self.traffic_data = TrafficData()
        self.loop = asyncio.get_event_loop()

    async def consumer_handler(self, websocket):
        while True:
            message = await websocket.recv()
            print("received", message)

    async def producer_handler(self, websocket):
        while True:
            message = await self.msg_queue.get()
            print('get value')
            await websocket.send(message)
            print("sent", message)

    async def handler(self, websocket, path):
        consumer_task = asyncio.ensure_future(self.consumer_handler(websocket))
        producer_task = asyncio.ensure_future(self.producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

    def _loop_in_thread(self, loop):
        start_server = websockets.serve(self.handler, 'localhost', 8765)
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_server)
        loop.run_forever()


    def start(self):
        t = threading.Thread(target=self._loop_in_thread, args=(self.loop,))
        t.start()

