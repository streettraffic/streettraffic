import math
from . import app_settings
import numpy as np
import pandas as pd
from PIL import Image
import requests
from io import BytesIO


# todo: convert quadkeys to tile
# todo: convert tile to coordinates
# todo:


def get_tile(lat: float, lon: float, zoom: int) -> tuple:
    """
    inputs: lat:float(latitue), lon:float(longitude), and zoom:int(zoom level)

    The function is used to generate column and row information for HERE API usage. For details, please
    visit https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/key-concepts.html
    for reference. 

    return :tuple(column, row)
    """
    lat_rad = lat * math.pi / 180
    n = math.pow(2, zoom)
    col = n * ((lon + 180) / 360)  # Column
    row = n * (1 - (math.log(math.tan(lat_rad) + 1 /
                             math.cos(lat_rad)) / math.pi)) / 2  # Row

    return (int(col), int(row))


def get_quadkeys(col: float, row: float, zoom: int) -> str:
    """
    inputs: col:float(column), row:float, zoom:int

    This function is used to encode (col, row, zoom) as quadkey. For details, refer to 
    https://developer.here.com/rest-apis/documentation/traffic/common/map_tile/topics/quadkeys.html

    return :str(quadkey)
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


def get_map_tile_resource(location_data: tuple, location_type: str, zoom: int, img_size: int) -> str:
    """
    inputs: location_data: tuple, zoom:int(zoom level), img_size:int(256 or 512), location_type: str

    The location_type and corresponding location data is as follow
    location_type = "latlon"; location_data = (latitude, longitude)
    location_type = "colrow"; location_data = (column, row)

    This function is uses location_data to generate (col, row), if location_type == "colrow", we simply use the provided
    (col, row) and further use them to generate a url to get map_tile. 

    For map_tile resource details, refer to
    https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/quick-start.html

    return :str(url for map_tile)
    """
    # if user did not provide a col, row, we use get_tile()
    if location_type == "latlon":
        (col, row) = get_tile(*location_data, zoom)
    elif location_type == "colrow":
        (col, row) = location_data

    total_url = app_settings.MAP_TILE_BASE_URL + str(zoom) + '/' + str(int(col)) + '/' + str(int(
        row)) + '/' + str(img_size) + '/png8?app_id=' + app_settings.APP_ID + '&app_code=' + app_settings.APP_CODE

    return total_url


def get_traffic_json_resource(location_data: tuple, location_type: str, zoom: int) -> str:
    """
    inputs: location_data: tuple, zoom:int(zoom level)
    default inputs: col:int = 0, row: int = 0, location_type: str

    The location_type and corresponding location data is as follow
    location_type = "latlon"; location_data = (latitude, longitude)
    location_type = "colrow"; location_data = (column, row)

    This function is uses location_data to generate (col, row), if location_type == "colrow", we simply use the provided
    (col, row). Then we use (col, row) to further utilize get_quadkeys() to 
    get a quad key, then generate a url to get traffic_json resource. 

    For traffic_json resource details, refer to
    https://developer.here.com/rest-apis/documentation/traffic/topics/quick-start.html

    return :str(url for traffic_tile_json)
    """
    if location_type == "latlon":
        (col, row) = get_tile(*location_data, zoom)
    elif location_type == "colrow":
        (col, row) = location_data

    quadkey = get_quadkeys(col, row, zoom)
    total_url = app_settings.JSON_TILE_BASE_URL + 'app_id=' + app_settings.APP_ID + \
        '&app_code=' + app_settings.APP_CODE + '&quadkey=' + quadkey + '&responseattributes=sh,fc'

    return total_url


def get_area_tile_matrix(cor1: tuple, cor2: tuple, zoom: int) -> pd.DataFrame:
    """
    inputs: cor1:tuple(coordinates: (latitue, longitude)) cor2: same as cor1
            zoom: int(zoom level)

    This function takes two coordinates and calculate their tile (col, row),
    then it generate a matrix of tiles to cover the square defined by those
    two coordinates.

    ###^^^^^^*####  (in this example, two coordinates are denoted as *
    #  ^^^^^^^   #   and this function should generate tile to cover the
    #  ^^^^^^^   #   area denoted by ^ and *)
    ###*^^^^^^####

    return :DataFrame(a matrix of tiles to cover the area spanned by two coordinates)
    """
    tile1 = get_tile(*cor1, zoom)  #(col, row)
    tile2 = get_tile(*cor2, zoom)  #(col, row)
    left_col = min(tile1[0], tile2[0])
    right_col = max(tile1[0], tile2[0])
    botom_row = min(tile1[1], tile2[1])
    top_row = max(tile1[1], tile2[1])
    matrix = pd.DataFrame(index = range(top_row - botom_row + 1), columns = range(right_col - left_col + 1))
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = (left_col + i, botom_row + j)

    return matrix

def get_area_tile_matrix_url(cor1: tuple, cor2: tuple, zoom: int) -> pd.DataFrame:
    """
    inputs: cor1:tuple(coordinates: (latitue, longitude)) cor2: same as cor1
            zoom: int(zoom level)

    This function takes two coordinates and calculate their tile (col, row),
    then it generate a matrix of tiles **URLs** to cover the square defined by those
    two coordinates.

    ###^^^^^^*####  (in this example, two coordinates are denoted as *
    #  ^^^^^^^   #   and this function should generate tile to cover the
    #  ^^^^^^^   #   area denoted by ^ and *)
    ###*^^^^^^####

    return :DataFrame(a matrix of tiles **URLs** to cover the area spanned by two coordinates)
    """
    matrix = get_area_tile_matrix(cor1, cor2, zoom)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = get_map_tile_resource(location_data = matrix[i][j], location_type = "colrow", zoom = zoom, img_size = 512)

    return matrix

def assemble_matrix_images(matrix: pd.DataFrame) -> pd.DataFrame:
    """
    input: matrix: pd.DataFrame, 

    This function takes a matrix generated by get_area_tile_matrix_url() and assemble a picture
    out of it. 

    return :pd.DataFrame(a matrix of PIL.Image classes)

    """
    img_matrix = matrix.copy(deep=True)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            response = requests.get(matrix[i][j])
            img_matrix[i][j] = Image.open(BytesIO(response.content))

    # producing image
    vertical = []
    for j in range(len(img_matrix)):
        horizontal_combs = np.hstack( (np.array(i.convert("RGB"))) for i in img_matrix.loc[j] )
        vertical += [horizontal_combs]
    imgs_comb = np.vstack(vertical)
    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.show()
    return img_matrix
