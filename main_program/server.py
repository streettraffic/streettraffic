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
            try:
                message = await websocket.recv()
                print("received", message)
            except websockets.exceptions.ConnectionClosed:
                print('disconnected')
                break

    async def producer_handler(self, websocket):
        while True:
            try:
                message = await self.msg_queue.get()
                print('get value')
                await websocket.send(message)
                print("sent", message)
            except websockets.exceptions.ConnectionClosed:
                print('disconnected')
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

    def _loop_in_thread(self, loop):
        start_server = websockets.serve(self.handler, 'localhost', 8765)
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_server)
        loop.run_forever()


    def start(self):
        t = threading.Thread(target=self._loop_in_thread, args=(self.loop,))
        t.start()
        print('server served at ws://127.0.0.1:8765/')

