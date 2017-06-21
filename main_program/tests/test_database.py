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

from ..map_resource import ultil
from .. import tools
from ..database import TrafficData
from ..datafeed import DataFeed


r.net.connection_type = r.net.DefaultConnection  # the default connection
traffic_data = TrafficData('test')


r.set_loop_type('asyncio')
data_feed = DataFeed('test')

def test_read_traffic_data():
    """ """
    global traffic_data
    data = traffic_data.read_traffic_data('https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303211003&responseattributes=sh,fc')
    assert len(data['RWS'][0]['RW'][0]['FIS'][0]['FI'][0]['SHP']) > 0


@pytest.mark.asyncio
async def test_insert_json_data():
    """ """
    global traffic_data
    global data_feed

    ## wait unitl data_feed starts to monitor database
    await data_feed.init()

    ## start inserting documents
    with open('test_data/test_traffic_data.json') as f:
        data = json.load(f)
    record = traffic_data.insert_json_data(data, 'test', True)

    ## wait the data_feed to close
    await data_feed.finishing()
    print('record',len(record))
    print('datafeed',len(data_feed.data))


def test_generate_geojson_collection():
    geojson_object1 = json.loads('{"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}')
    geojson_object2 = json.loads('{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}')
    geojson_combined_test = json.loads('{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}, {"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}]}')
    geojson_combined = TrafficData.generate_geojson_collection([geojson_object2, geojson_object1])

    assert geojson_combined == geojson_combined_test

def test_fetch_geojson_item():
    """
    hard to test since our database is still under changing development
    """
    #print(traffic_data)
    pass