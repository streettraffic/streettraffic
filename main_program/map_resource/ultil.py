import math
import numpy as np
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from geopy.distance import vincenty, great_circle
from matplotlib.path import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List

from . import app_settings


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


def produce_polygon(polygon_ordered_coordinates: List, zoom: int, plot_polygon = True) -> Path:
    """
    inputs: 
    polygon_ordered_coordinates: List(an ordered list of points that composes a polygon)
    plot_polygon = True
    zoom: int
    example inputs:
    [[25.890099, -80.264561], [25.851873, -80.308744], [25.81123, -80.248538], [25.848596, -80.215765]], True


    This function use matplotlib.path to create a Path/polygon object. Later we can use
    this Path/polygon object to invoke Path.contains_point() method. For more details 
    on contains_point(), refer to 
    https://stackoverflow.com/questions/21328854/shapely-and-matplotlib-point-in-polygon-not-accurate-with-geolocation

    If plot_polygon == True, we use matplotlib to plot the polygon
    """
    polygon_tile_points = []
    for item in polygon_ordered_coordinates:
        polygon_tile_points += [get_tile(*item, zoom)]
    polygon_tile_points += [polygon_tile_points[0]]
    polygon = Path(polygon_tile_points)
    if plot_polygon:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        patch = patches.PathPatch(polygon, facecolor='orange', lw=2)
        ax.add_patch(patch)
        ax.set_xlim(min(polygon_tile_points, key = lambda item: item[0])[0], max(polygon_tile_points, key = lambda item: item[0])[0])
        ax.set_ylim(min(polygon_tile_points, key = lambda item: item[1])[1], max(polygon_tile_points, key = lambda item: item[1])[1])
        plt.show()
    return polygon

def get_area_tile_matrix(list_points: List, zoom: int, use_polygon = False) -> pd.DataFrame:
    """
    inputs: list_points (GPS coordinates that you want to add)
            zoom: int(zoom level)
            use_polygon = None

    example inputs: [(33.766764, -84.409533), (33.740003, -84.368978)], 14

    This function takes the coordinates from *args and calculate their tile (col, row),
    then it generate a matrix of tiles to cover the square defined by those coordinates.

    If use_polygon == True, then we generate a polygon given by produce_polygon,
    and further return the area_tiles that are **inside**(not including boundry) the polygon

    ###^^^^^^*####  (in this example, two coordinates are denoted as *
    #  ^^^^^^^   #   and this function should generate tile to cover the
    #  ^^^^^^^   #   area denoted by ^ and *)
    ###*^^^^^^####

    return :DataFrame(a matrix of tiles to cover the area spanned by two coordinates)
    """
    tiles = []
    for point in list_points:
        tiles += [get_tile(*point, zoom)]
    left_col = min(tiles, key = lambda item: item[0])[0]
    right_col = max(tiles, key = lambda item: item[0])[0]
    top_row = min(tiles, key = lambda item: item[1])[1]
    bottom_row = max(tiles, key = lambda item: item[1])[1]  # notice bottom_row would actually have a higher number
    matrix = pd.DataFrame(index = range(bottom_row - top_row + 1), columns = range(right_col - left_col + 1))
    for row in range(len(matrix)):
        for col in range(len(matrix.iloc[0])):
            matrix.iloc[row,col] = (left_col + col, top_row + row)

    if use_polygon:
        polygon = produce_polygon(list_points, zoom, plot_polygon = False)
        for row in range(len(matrix)):
            for col in range(len(matrix.iloc[0])):
                if not polygon.contains_point(matrix.iloc[row,col]):
                    matrix.iloc[row,col] = None

    return matrix



def get_area_tile_matrix_url(resource_type: str, list_points: List, zoom: int, use_polygon = False) -> pd.DataFrame:
    """
    inputs: resource_type: str(a string indicating the resource type)
            list_points (GPS coordinates that you want to add)
            zoom: int(zoom level)
            use_polygon = False

    The resource_type has two options:
    * map_tile
    * traffic_json

    This function takes two coordinates and calculate their tile (col, row),
    then it generate a matrix of tiles **URLs** (either map_tile urls or traffic_json urls) 
    to cover the square defined by those two coordinates.

    ###^^^^^^*####  (in this example, two coordinates are denoted as *
    #  ^^^^^^^   #   and this function should generate tile to cover the
    #  ^^^^^^^   #   area denoted by ^ and *)
    ###*^^^^^^####

    return :DataFrame(a matrix of tiles **URLs** to cover the area spanned by two coordinates)
    """
    matrix = get_area_tile_matrix(list_points, zoom, use_polygon)
    for row in range(len(matrix)):
        for col in range(len(matrix.iloc[0])):
            if matrix.iloc[row,col]:
                if resource_type == "map_tile":
                    matrix.iloc[row,col] = get_map_tile_resource(location_data = matrix.iloc[row,col], location_type = "colrow", zoom = zoom, img_size = 512)
                elif resource_type == "traffic_json":
                    matrix.iloc[row,col] = get_traffic_json_resource(location_data = matrix.iloc[row,col], location_type = "colrow", zoom = zoom)

    return matrix

def assemble_matrix_images(matrix: pd.DataFrame) -> pd.DataFrame:
    """
    input: matrix: pd.DataFrame, 

    This function takes a matrix generated by get_area_tile_matrix_url() and assemble a picture
    out of it. 

    return :pd.DataFrame(a matrix of PIL.Image classes)

    """
    img_matrix = matrix.copy(deep=True)
    for row in range(len(matrix)):
        for col in range(len(matrix.iloc[0])):
            if matrix.iloc[row,col]:
                response = requests.get(matrix.iloc[row,col])
                img_matrix.iloc[row,col] = Image.open(BytesIO(response.content))

    # producing image
    vertical = []
    for row in range(len(img_matrix)):
        hstack_list = []
        for item in img_matrix.iloc[row]:
            if item:
                hstack_list += [(np.array(item.convert("RGB")))]
            else:
                hstack_list += [np.zeros((512,512,3), dtype= np.uint8)]
        horizontal_combs = np.hstack(hstack_list)
        vertical += [horizontal_combs]
    imgs_comb = np.vstack(vertical)
    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.show()
    return img_matrix

def get_distance(point1: tuple, point2: tuple, location_type:str = "latlon", distance_formula:str = "great_circle", unit:str = "meters") -> float:
    """
    inputs: point1: tuple, point2: tuple, location_type:str = "latlon", distance_formula:str = "great_circle", unit:str = "meters"
    the format should be point1 = (latitude, longitude)
    currently only supporting location_type = "latlon"
    distance_formula has two option: "great_circle" and "vincenty"
    the defualt unit is meters

    This function is a quick wraper for geopy.

    return the distance between point1 and point2
    """
    if distance_formula == "great_circle":
        return great_circle(point1, point2).meters
    elif distance_formula == "vincenty":
        return vincenty(point1, point2).meters
    else:
        raise Exception('undefined distance_formula')
