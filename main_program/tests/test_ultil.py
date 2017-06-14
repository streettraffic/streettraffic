from ..map_resource import ultil
from .. import tools
import pandas as pd


def test_get_tile():
    """
    The official example provided by HERE
    https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/key-concepts.html
    """
    assert ultil.get_tile(52.525439, 13.38727, 12) == (2200, 1343)


def test_get_quadkeys():
    """
    The official example provided by HERE
    https://developer.here.com/rest-apis/documentation/traffic/common/map_tile/topics/quadkeys.html
    """
    assert ultil.get_quadkeys(35210, 21493, 16) == "1202102332221212"


def test_get_map_tile_resource():
    assert ultil.get_map_tile_resource((33.670156, -84.325984),"latlon", 14, 512) == \
    'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4354/6562/512/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw'

    assert ultil.get_map_tile_resource((4354, 6562),"colrow", 14, 512) == \
    'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4354/6562/512/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw'

def test_get_traffic_json_resource():
    assert ultil.get_traffic_json_resource((34.9237, -82.4383), "latlon", 14) == \
    'https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&responseattributes=sh,fc'

    assert ultil.get_traffic_json_resource((4440, 6493), "colrow", 14) == \
    'https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&responseattributes=sh,fc'

def test_get_area_tile_matrix():
    df = pd.DataFrame([[(4350, 6557),(4351, 6557),(4352, 6557)],
                       [(4350, 6558),(4351, 6558),(4352, 6558)],
                       [(4350, 6559),(4351, 6559),(4352, 6559)]])
    assert df.equals(ultil.get_area_tile_matrix((33.766764, -84.409533), (33.740003, -84.368978), 14))

def test_get_area_tile_matrix_url():
    df = tools.load_data_object("test_data/get_area_tile_matrix_url() for map_tile.pkl")
    cor1 = (33.766764, -84.409533)
    cor2 = (33.740003, -84.368978)
    info = ultil.get_area_tile_matrix(cor1, cor2, 14)
    matrix = ultil.get_area_tile_matrix_url("map_tile", cor1, cor2, 14)
    assert df.equals(matrix)