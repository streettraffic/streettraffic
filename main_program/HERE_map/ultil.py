import math
from . import app_settings

# todo: convert quadkeys to tile
# todo: convert tile to coordinates
# todo:


def get_tile(lat: float, lon: float, zoom: float) -> tuple:
    """
    inputs: lat:float(latitue), lon:float(longitude), and zoom:float(zoom level)

    The function is used to generate column and row information for HERE API usage. For details, please
    visit https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/key-concepts.html
    for reference. 

    return: :tuple(column, row)
    """
    lat_rad = lat * math.pi / 180
    n = math.pow(2, zoom)
    col = n * ((lon + 180) / 360)  # Column
    row = n * (1 - (math.log(math.tan(lat_rad) + 1 /
                             math.cos(lat_rad)) / math.pi)) / 2  # Row

    return (int(col), int(row))


def get_quadkeys(col: float, row: float, zoom: float) -> str:
    """
    inputs: col:float(column), row:float, zoom:float

    This function is used to encode (col, row, zoom) as quadkey. For details, refer to 
    https://developer.here.com/rest-apis/documentation/traffic/common/map_tile/topics/quadkeys.html

    return: :str(quadkey)
    """
    quadkey = ""
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if (col & mask) != 0:  # notice this is a bitwise operator!! different from && or and
            digit += 1
        if (row & mask) != 0:
            digit += 2
        quadkey += str(digit)

    return quadkey


def get_map_tile_resource(lat: float, lon: float, zoom: float, img_size: int) -> str:
    """
    inputs: lat:float(latitue), lon:float(longitude), zoom:float(zoom level), img_size:int(256 or 512)

    This function is uses get_tile() function to get (col, row) and further use them to 
    generate a url to get map_tile. For map_tile resource details, refer to
    https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/quick-start.html

    return: :str(url for map_tile)
    """
    (col, row) = get_tile(lat, lon, zoom)
    total_url = app_settings.MAP_TILE_BASE_URL + str(zoom) + '/' + str(int(col)) + '/' + str(int(
        row)) + '/' + str(img_size) + '/png8?app_id=' + app_settings.APP_ID + '&app_code=' + app_settings.APP_CODE

    return total_url


def get_traffic_json_resource(lat: float, lon: float, zoom: float) -> str:
    """
    inputs: lat:float(latitue), lon:float(longitude), zoom:float(zoom level)

    This function is uses get_tile() function to get (col, row) and use further use get_quadkeys to 
    get a quad key, then generate a url to get traffic_json resource. For traffic_json resource details, refer to
    https://developer.here.com/rest-apis/documentation/traffic/topics/quick-start.html

    return: :str(url for map_tile)
    """
    (col, row) = get_tile(lat, lon, zoom)
    quadkey = get_quadkeys(col, row, zoom)
    total_url = app_settings.JSON_TILE_BASE_URL + 'app_id=' + app_settings.APP_ID + \
        '&app_code=' + app_settings.APP_CODE + '&quadkey=' + quadkey

    return total_url
