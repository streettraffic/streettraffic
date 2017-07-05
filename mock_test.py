# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 22:11:58 2017

@author: costa
"""
from unittest import mock
import json
import rethinkdb as r
import time
import asyncio
import websockets
import datetime


## import custom module
import main_program
from main_program.map_resource import ultil
from main_program.database import TrafficData
from main_program import tools
from main_program.server import TrafficServer

class _iter:

    def __init__(self, data):
        """
        data should be a list
        """
        self.data = data
        self.index = 0

    def next(self):
        try:
            data = self.data[self.index]
            self.index += 1
            return data
        except Exception as e:
            raise Exception('_iter error, no next')
            
    def __iter__(self):
        for item in self.data:
            yield self.next()

def mocked_run_side_effect(self, *args, **kwargs):
    """
    In this function we are going to mock the return of database
    """
    print('self',type(self))
    print(self)
    print('args',args)
    if self.__str__() == """r.table('road_data').get('["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]')""":
        print('**road_data called**')
        return {
            'FC': 2,
            'flow_item_id': '{"DE": "University Ave/Exit 244", "LE": 1.57367, "PC": 4117, "QD": "-"}',
            'geometry': {'$reql_type$': 'GEOMETRY',
            'coordinates': [
                [-84.40353, 33.70524],
                [-84.40347, 33.70551],
                [-84.40335, 33.70597]],
            'type': 'LineString'},
            'road_data_id': '["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]',
            'value': ['33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 ']
        }

    elif self.__str__() == """r.table('flow_item').get('{"DE": "University Ave/Exit 244", "LE": 1.57367, "PC": 4117, "QD": "-"}')""":
        print('**flow_item called**')
        return {
            'CF': 'See table flow_data',
            'SHP': 'See table road_data',
            'TMC': {
                'DE': 'University Ave/Exit 244',
                'LE': 1.57367,
                'PC': 4117,
                'QD': '-'
            },
            'flow_item_id': '{"DE": "University Ave/Exit 244", "LE": 1.57367, "PC": 4117, "QD": "-"}'
        }

    elif self.__str__() == """r.table('flow_data').get_all(['{"DE": "University Ave/Exit 244", "LE": 1.57367, "PC": 4117, "QD": "-"}', '0e8e60c5-3936-41f0-86fc-3b6e0e37ac4a'], index='flow_crawled_batch').limit(3)""":
        print('**flow_data called**')
        return _iter([{
            'CN': 0.99,
            'FF': 55.3,
            'JF': 7.48248,
            'LN': [],
            'SP': 21.01,
            'SSS': {'SS': [{'FF': 54.68,
               'JF': 8.00539,
               'LE': 0.33,
               'LN': [],
               'SP': 18.18,
               'SU': 18.18},
              {'FF': 54.68,
               'JF': 7.31136,
               'LE': 1.24,
               'LN': [],
               'SP': 21.94,
               'SU': 21.94}]},
            'SU': 21.01,
            'TY': 'TR',
            'crawled_batch_id': '0e8e60c5-3936-41f0-86fc-3b6e0e37ac4a',
            'created_timestamp': datetime.datetime(2017, 6, 26, 11, 30, 26, tzinfo=r.ast.RqlTzinfo('00:00')),
            'flow_data_id': 'c83be85a-40df-47ae-a21e-e8f662cee8d2',
            'flow_item_id': '{"DE": "University Ave/Exit 244", "LE": 1.57367, "PC": 4117, "QD": "-"}',
            'original_data_id': 'cbded591-1554-4eba-9294-d21a732fd2e3'
        }])

    elif self.__str__() == """r.table('road_data').get('["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]')['geometry'].to_geojson()""":
        return {
            'coordinates': [[-84.40353, 33.70524],
              [-84.40347, 33.70551],
              [-84.40335, 33.70597]],
            'type': 'LineString'
        }

#r = mock.MagicMock(name = "rethinkdb")
#r.connect.return_value.run.side_effect = my_side_effect
run = mock.Mock(name = "run")
run.return_value.side_effect = mocked_run_side_effect

#r.connect.return_value = True
#conn = r.connect('localhost', 28015)

traffic_server = TrafficServer(database_name= "Traffic", database_ip = "localhost")
traffic_server.start()
conn = traffic_server.traffic_data.conn

@mock.patch('main_program.database.r.RqlQuery.run', run)
def test():
	traffic_server.traffic_data.fetch_geojson_item('xiix', 'haha')

@mock.patch.object(main_program.database.r.RqlQuery, 'run', autospec=True)
def test1(mocked_run):
    mocked_run.side_effect = mocked_run_side_effect
    traffic_server.traffic_data.fetch_geojson_item('["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]', '0e8e60c5-3936-41f0-86fc-3b6e0e37ac4a')
    
## this works
#with mock.patch.object(main_program.database.r.RqlQuery, 'run', autospec=True) as mock_foo:
#  mock_foo.side_effect = my_side_effect
#  x = r.db('Traffic').table('xiix')
#  k = x.run()