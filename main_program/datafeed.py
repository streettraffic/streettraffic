import asyncio
import threading
import rethinkdb as r
from typing import List
import time



class DataFeed:

    def __init__(self, database_name: str = "Traffic"):
        self.data = {}
        self.database_name = database_name
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)
        self.thread = threading.Thread(target=self._loop_in_thread)
        self.task_list = []


    async def init(self):
        """
        This class establishes a connection towards the database
        """
        self.running = self.loop.create_future()
        self.initialized = self.loop.create_future()
        self.conn = await r.connect('localhost', 28015)
        self.data = {}
        if self.database_name in await r.db_list().run(self.conn):
            self.conn.use(self.database_name)
        else:
            await self.db_create(self.database_name).run(self.conn)
            self.conn.use(self.database_name)

        self.set_feed_data_type(['flow_data','road_data', 'original_data', 'crawled_batch'])
        print('========setting data type========')
        self.loop.call_soon_threadsafe(self.loop.create_task, self.monitor_flow_data_feed('original_data'))
        self.loop.call_soon_threadsafe(self.loop.create_task, self.monitor_flow_data_feed('flow_data')) 
        self.loop.call_soon_threadsafe(self.loop.create_task, self.monitor_flow_data_feed('road_data')) 
        self.loop.call_soon_threadsafe(self.loop.create_task, self.monitor_flow_data_feed('crawled_batch')) 

    async def monitor_flow_data_feed(self, tablename: str):
        """
        """
        print('monitoring', tablename)
        data_feed = await r.db('test').table(tablename).changes().run(self.conn)
        while await data_feed.fetch_next():
            self.data[tablename] += [await data_feed.next()]

    def set_feed_data_type(self, tablename_list: List):
        """
        """
        for tablename in tablename_list:
            self.data[tablename] = []

    def _loop_in_thread(self):
        """
        """
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self.init())
        self.loop.run_forever()

    def start(self):
        """
        """
        self.thread.start()
        print('datafeed running')

    async def finishing(self):
        await self.loop.shutdown_asyncgens()


    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.create_task, self._prepare_stop())
