"""
Before run this test_database.py, we have to import our test_database.
use command
> rethinkdb restore test_database.gz
to restore our test_database
"""

import pytest
import pandas as pd
import json
import rethinkdb as r
import asyncio
from unittest import mock
import datetime

from ..map_resource import ultil
from .. import tools
from ..database import TrafficData
from .. import database
from ..datafeed import DataFeed


class _iter:

    def __init__(self, data):
        """
        data should be a list
        """
        self.data = data
        self.index = 0

    def next(self):
        try:
            return self.data[self.index]
            self.index += 1
        except Exception as e:
            raise Exception('_iter error, no next')


r.net.connection_type = r.net.DefaultConnection  # the default connection
traffic_data = TrafficData('test')


r.set_loop_type('asyncio')
data_feed = DataFeed('test')

@pytest.mark.asyncio
async def insert_json_data():
    """ """
    global traffic_data
    global data_feed

    ## wait unitl data_feed starts to monitor database
    data_feed.loop = asyncio.get_event_loop()
    await data_feed.init()
    print('setting up')
    await asyncio.sleep(2)  # wait initialization
    print('finished setting monitoring')


    ## start inserting documents
    with open('test_data/test_traffic_data.json', encoding='utf-8') as f:
        data = json.load(f)
    traffic_data.insert_json_data(data, 'test', True)

    tested_data = tools.load_data_object('test_data/test_insert_json_data.dict')
    print('load inserted data')
    await asyncio.sleep(5)

    ## wait the data_feed to close
    await data_feed.finishing()
    print('datafeed',len(data_feed.data))

    ## delete every document we have inserted from this function
    for item in data_feed.data['original_data']:
        original_data_id = item['new_val']['id']
        r.db('test').table('original_data').get(original_data_id).delete().run(traffic_data.conn)
    
    for item in data_feed.data['road_data']:
        road_data_id = item['new_val']['id']
        r.db('test').table('road_data').get(road_data_id).delete().run(traffic_data.conn)
    
    for item in data_feed.data['flow_data']:
        flow_data_id = item['new_val']['id']
        r.db('test').table('flow_data').get(flow_data_id).delete().run(traffic_data.conn)

    print('deleted')


    assert len(data_feed.data['original_data']) == len(tested_data['original_data'])
    assert len(data_feed.data['road_data']) == len(tested_data['road_data'])
    assert len(data_feed.data['flow_data']) == len(tested_data['flow_data'])
    assert len(data_feed.data['crawled_batch']) == len(tested_data['crawled_batch'])

def test_parse_SHP_values():
    global traffic_data
    assert traffic_data.parse_SHP_values(["34.9495,-82.43912 34.94999,-82.4392 34.95139,-82.4394 "]) == [[-82.43912, 34.9495], [-82.4392, 34.94999], [-82.4394, 34.95139]]

def test_read_traffic_data():
    """ """
    global traffic_data
    data = traffic_data.read_traffic_data('https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303211003&responseattributes=sh,fc')
    data2 = traffic_data.read_traffic_data('https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200333211030&responseattributes=sh,fc')
    assert len(data['RWS'][0]['RW'][0]['FIS'][0]['FI'][0]['SHP']) > 0
    assert data2 == None

def helper_create_tables():
    """ maybe not needed"""
    pass

def store_matrix_json():
    """ maybe not needed"""
    pass

@mock.patch.object(database.r.RqlQuery, 'run', autospec = True)
def test_fetch_geojson_item(mocked_run):
    """
    We mocked RqlQuery.run()  An example of RqlQuery is r.db('Traffic').table('test'), RqlQuery doesn't return anything
    until you do r.db('Traffic').table('test').run()


    """
    global traffic_data
    def mocked_run_side_effect(self, *args, **kwargs):
        """
        In this function we are going to mock the return of database

        mock.side_effect enables you to conditionally return values based on inputs. 
        """
        if self.__str__() == """r.table('road_data').get('["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]')""":
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

    mocked_run.side_effect = mocked_run_side_effect # pass the custome mocked_run funtion to mocked_run
    assert traffic_data.fetch_geojson_item('["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]', '0e8e60c5-3936-41f0-86fc-3b6e0e37ac4a') == {
        'geometry': {'coordinates': [[-84.40353, 33.70524],
           [-84.40347, 33.70551],
           [-84.40335, 33.70597]],
          'type': 'LineString'},
         'properties': {'CF': {'CN': 0.99,
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
           'created_timestamp': '2017-06-26T11:30:26+00:00',
           'flow_data_id': 'c83be85a-40df-47ae-a21e-e8f662cee8d2',
           'flow_item_id': '{"DE": "University Ave/Exit 244", "LE": 1.57367, "PC": 4117, "QD": "-"}',
           'original_data_id': 'cbded591-1554-4eba-9294-d21a732fd2e3'},
          'TMC': {'DE': 'University Ave/Exit 244',
           'LE': 1.57367,
           'PC': 4117,
           'QD': '-'},
          'color': 'yellow'},
         'type': 'Feature'
    }


def test_generate_geojson_collection():
    geojson_object1 = json.loads('{"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}')
    geojson_object2 = json.loads('{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}')
    geojson_combined_test = json.loads('{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}, {"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}]}')
    geojson_combined = TrafficData.generate_geojson_collection([geojson_object2, geojson_object1])

    assert geojson_combined == geojson_combined_test

def traffic_flow_color_scheme():
    """ maybe not needed """
    pass

def test_get_nearest_road():
    global traffic_data
    assert traffic_data.get_nearest_road((33.70524, -84.40353), max_dist= 10) == json.loads('{"dist": 0, "doc": {"FC": 2, "flow_item_id": "{\\"DE\\": \\"University Ave/Exit 244\\", \\"LE\\": 1.57367, \\"PC\\": 4117, \\"QD\\": \\"-\\"}", "geometry": {"$reql_type$": "GEOMETRY", "coordinates": [[-84.40353, 33.70524], [-84.40347, 33.70551], [-84.40335, 33.70597]], "type": "LineString"}, "road_data_id": "[\\"33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 \\"]", "value": ["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]}}')

def get_historic_traffic():
    pass

def test_get_historic_batch():
    global traffic_data
    assert traffic_data.get_historic_batch() == [{'crawled_batch_id': '3962491e-8cb0-4685-9884-8cb292240def',
                                                    'crawled_timestamp': '2017-06-23T20:16:02.027000+00:00'},
                                                {'crawled_batch_id': 'cfebf60f-2624-4001-8284-78598d3662f9',
                                                    'crawled_timestamp': '2017-06-23T20:01:47.862000+00:00'}]
