from ..map_resource import ultil
from .. import tools
from ..database import TrafficData
import pandas as pd
import json

def test_generate_geojson_collection():
    geojson_object1 = json.loads('{"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}')
    geojson_object2 = json.loads('{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}')
    geojson_combined_test = json.loads('{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"coordinates": [[-82.42968, 34.92954], [-82.43003, 34.92729]], "type": "LineString"}, "properties": {"TMC": {"DE": "US-25-BR/US-276/Poinsett Hwy", "LE": 1.87469, "PC": 10933, "QD": "+"}, "CF": {"CN": 0.7, "FF": 41.01, "JF": 1.89393, "LN": [], "SP": 31.69, "SU": 31.69, "TY": "TR"}}}, {"type": "Feature", "geometry": {"coordinates": [[-82.42907, 34.91623], [-82.42911, 34.91647], [-82.42917, 34.91684]], "type": "LineString"}, "properties": {"TMC": {"DE": "Old Buncombe Rd", "LE": 1.67396, "PC": 10934, "QD": "-"}, "CF": {"CN": 0.7, "FF": 42.25, "JF": 1.71568, "LN": [], "SP": 33.55, "SU": 33.55, "TY": "TR"}}}]}')
    geojson_combined = TrafficData.generate_geojson_collection([geojson_object2, geojson_object1])

    assert geojson_combined == geojson_combined_test