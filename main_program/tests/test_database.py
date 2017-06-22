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

from ..map_resource import ultil
from .. import tools
from ..database import TrafficData
from ..datafeed import DataFeed


r.net.connection_type = r.net.DefaultConnection  # the default connection
traffic_data = TrafficData('test')


r.set_loop_type('asyncio')
data_feed = DataFeed('test')

@pytest.mark.asyncio
async def test_insert_json_data():
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

def test_read_traffic_data():
    """ """
    global traffic_data
    data = traffic_data.read_traffic_data('https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303211003&responseattributes=sh,fc')
    data2 = traffic_data.read_traffic_data('https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200333211030&responseattributes=sh,fc')
    assert len(data['RWS'][0]['RW'][0]['FIS'][0]['FI'][0]['SHP']) > 0
    assert data2 == None


def test_parse_SHP_values():
    global traffic_data
    assert traffic_data.parse_SHP_values(["34.9495,-82.43912 34.94999,-82.4392 34.95139,-82.4394 "]) == [[-82.43912, 34.9495], [-82.4392, 34.94999], [-82.4394, 34.95139]]


def store_matrix_json():
    """ maybe not needed"""
    pass

def test_fetch_geojson_item():
    global traffic_data
    assert traffic_data.fetch_geojson_item('["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]') == json.loads('{"type": "Feature", "geometry": {"coordinates": [[-84.40353, 33.70524], [-84.40347, 33.70551], [-84.40335, 33.70597]], "type": "LineString"}, "properties": {"TMC": {"DE": "University Ave/Exit 244", "LE": 1.57367, "PC": 4117, "QD": "-"}, "CF": {"CN": 0.99, "FF": 55.3, "JF": 9.05158, "LN": [], "SP": 9.65, "SU": 9.65, "TY": "TR", "crawled_batch_id": "c1c9cf8c-e4d5-41e3-977c-aee7b3a7043d", "created_timestamp": "2017-06-20T20:01:34+00:00", "original_data_id": "6b9bdfce-62da-4c5a-9ced-9166771f2dd9"}, "color": "red"}}')

def test_generate_geojson_collection():
    geojson_object1 = json.loads('{"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}')
    geojson_object2 = json.loads('{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}')
    geojson_combined_test = json.loads('{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}, {"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}]}')
    geojson_combined = TrafficData.generate_geojson_collection([geojson_object2, geojson_object1])

    assert geojson_combined == geojson_combined_test

def test_get_nearest_road():
    global traffic_data
    assert traffic_data.get_nearest_road((33.70524, -84.40353), max_dist= 10) == json.loads('{"dist": 0, "doc": {"FC": 2, "flow_data_id": "{\\"DE\\": \\"University Ave/Exit 244\\", \\"LE\\": 1.57367, \\"PC\\": 4117, \\"QD\\": \\"-\\"}", "geometry": {"$reql_type$": "GEOMETRY", "coordinates": [[-84.40353, 33.70524], [-84.40347, 33.70551], [-84.40335, 33.70597]], "type": "LineString"}, "id": "[\\"33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 \\"]", "value": ["33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "]}}')

def get_historic_traffic():
    pass

def test_get_historic_batch():
    global traffic_data
    assert traffic_data.get_historic_batch() == [{'crawled_timestamp': '2017-06-20T20:02:32.491000+00:00',
                                                'id': 'c1c9cf8c-e4d5-41e3-977c-aee7b3a7043d'},
                                                {'crawled_timestamp': '2017-06-20T19:48:38.512000+00:00',
                                                'id': '8b5d54f6-1381-4eef-9080-25075ad19abe'},
                                                {'crawled_timestamp': '2017-06-20T19:05:13.668000+00:00',
                                                'id': '6dcfea39-e0e0-47e5-b8cc-2d20e1acbd46'}]
