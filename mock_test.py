# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 22:11:58 2017

@author: costa
"""
from unittest import mock
import json
# import rethinkdb as r
import time
import datetime as dt
import asyncio
import websockets


## import custom module
from main_program.map_resource import ultil
from main_program.database import TrafficData
from main_program import tools
from main_program.server import TrafficServer

def my_side_effect(*args, **kwargs):
	print(args)

r = mock.MagicMock(name = "rethinkdb")
r.connect.return_value.run.side_effect = my_side_effect

#r.connect.return_value = True
conn = r.connect('localhost', 28015)

traffic_server = TrafficServer(database_name= "Traffic", database_ip = "localhost")
traffic_server.start()
conn = traffic_server.traffic_data.conn

@mock.patch('main_program.database.r', r)
def test():
	traffic_server.traffic_data.fetch_geojson_item('xiix', 'haha')
	


