from ..map_resource.utility import Utility
from .. import tools
import pandas as pd

settings = {
    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
}

util = Utility(settings)

def test_get_tile():
    """
    The official example provided by HERE
    https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/key-concepts.html
    """
    assert util.get_tile(52.525439, 13.38727, 12) == [2200, 1343]


def test_get_quadkeys():
    """
    The official example provided by HERE
    https://developer.here.com/rest-apis/documentation/traffic/common/map_tile/topics/quadkeys.html
    """
    assert util.get_quadkeys(35210, 21493, 16) == "1202102332221212"


def test_get_map_tile_resource():
    assert util.get_map_tile_resource((33.670156, -84.325984),"latlon", 14, 512) == \
    'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4354/6562/512/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw'

    assert util.get_map_tile_resource((4354, 6562),"colrow", 14, 512) == \
    'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4354/6562/512/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw'

def test_get_traffic_json_resource():
    assert util.get_traffic_json_resource((34.9237, -82.4383), "latlon", 14) == \
    'https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&responseattributes=sh,fc'

    assert util.get_traffic_json_resource((4440, 6493), "colrow", 14) == \
    'https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&responseattributes=sh,fc'

def test_get_area_tile_matrix():
    df1 = pd.DataFrame([[(4350, 6557),(4351, 6557),(4352, 6557)],
                       [(4350, 6558),(4351, 6558),(4352, 6558)],
                       [(4350, 6559),(4351, 6559),(4352, 6559)]])

    df2 = pd.DataFrame([[(4350, 6558),(4351, 6558),(4352, 6558)],
                       [(4350, 6559),(4351, 6559),(4352, 6559)]])

    df3 = pd.DataFrame([[(4351, 6557),(4352, 6557)],
                       [(4351, 6558),(4352, 6558)],
                       [(4351, 6559),(4352, 6559)]])
    assert df1.equals(util.get_area_tile_matrix([(33.766764, -84.409533), (33.740003, -84.368978)], 14))
    assert df2.equals(util.get_area_tile_matrix([(33.741455, -84.397218), (33.744203, -84.369581)], 14))  # asymmetrical case 1
    assert df3.equals(util.get_area_tile_matrix([(33.728999, -84.395856), (33.775902, -84.363917)], 14))  # asymmetrical case 2


def test_get_area_tile_matrix_url():
    df = tools.load_data_object("test_data/get_area_tile_matrix_url() for map_tile.pkl")
    cor1 = (33.766764, -84.409533)
    cor2 = (33.740003, -84.368978)
    info = util.get_area_tile_matrix([cor1, cor2], 14)
    matrix = util.get_area_tile_matrix_url("map_tile", [cor1, cor2], 14)
    assert df.equals(matrix)

def test_get_distance():
    assert util.get_distance((33.70524,-84.40353), (33.71337,-84.39347)) == 1297.72758534478 

def test_read_geojson_polygon():
    assert util.read_geojson_polygon('{ "type": "FeatureCollection", "features": [ { "type": "Feature", "geometry": { "type": "Polygon", "coordinates": [ [ [ -84.39285278320312, 33.76266589608855 ], [ -84.3738842010498, 33.770015152780125 ], [ -84.3610954284668, 33.7613101391079 ], [ -84.37019348144531, 33.74468253332004 ], [ -84.38830375671387, 33.751391054166746 ], [ -84.39705848693848, 33.758384485188 ], [ -84.39285278320312, 33.76266589608855 ] ] ] }, "properties": {} } ] }') == [[33.76266589608855,-84.39285278320312],[33.770015152780125,-84.3738842010498],[33.7613101391079,-84.3610954284668],[33.74468253332004,-84.37019348144531],[33.751391054166746,-84.38830375671387],[33.758384485188,-84.39705848693848],[33.76266589608855,-84.39285278320312]]