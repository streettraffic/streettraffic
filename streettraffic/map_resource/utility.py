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
from typing import List, Dict
import json
import os


# todo: convert quadkeys to tile
# todo: convert tile to coordinates
# todo:

class Utility:

    """This class has some utility function for map resources

    In order to generate Url Resources, you should get app_id and app_code at developer.HERE.com
    Specific instructions can be found here:
    https://developer.here.com/rest-apis/documentation/traffic/common/credentials.html

    Attributes:
        app_id (str): The app id acquired from https://developer.here.com/
        app_code (str): The app code acquired from https://developer.here.com/
        map_tile_base_url (str): the base url of the map image tile requests
            an exmaple can be found here: https://developer.here.com/api-explorer/rest/traffic/traffic-tile
        json_tile_base_url (str): the base url of the traffic json tile requests
            an example can be found here: https://developer.here.com/api-explorer/rest/traffic/traffic-flow-quadkey

    Args:
        settings (Dict): The settings of your app

    Example:
        >>> settings = {
                'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
                'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
                'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
                'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
            }
        >>> util = Utility(settings)
        >>> util.app_id
        'F8aPRXcW3MmyUvQ8Z3J9'
    """

    def __init__(self, settings: Dict) -> None:
        """
        Args:
            settings (Dict): The settings of your app
        """
        self.app_id = settings['app_id']
        self.app_code = settings['app_code']
        self.map_tile_base_url = settings['map_tile_base_url']
        self.json_tile_base_url = settings['json_tile_base_url']

    @staticmethod
    def get_tile(lat: float, lon: float, zoom: int) -> List:
        """Given a GPS coordiante and zoom level, generate column and row information for HERE API usage. For details, please
        visit https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/key-concepts.html
        for reference.

        Args:
            lat (float): latitue
            lon (float): longitude
            zoom (int): the zoom level

        Returns:
            List: [col, row]

        Example:
            >>> # or checkout the unittest for this function
            >>> settings = {
                    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
                    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
                    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
                    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
                }
            >>> util = Utility(settings)
            >>> util.get_tile(52.525439, 13.38727, 12)
            [2200, 1343]
        """
        lat_rad = lat * math.pi / 180
        n = math.pow(2, zoom)
        col = n * ((lon + 180) / 360)  # Column
        row = n * (1 - (math.log(math.tan(lat_rad) + 1 /
                                 math.cos(lat_rad)) / math.pi)) / 2  # Row

        return [int(col), int(row)]

    @staticmethod
    def get_quadkeys(col: int, row: int, zoom: int) -> str:
        """This function is used to encode (col, row, zoom) as quadkey. For details, refer to
        https://developer.here.com/rest-apis/documentation/traffic/common/map_tile/topics/quadkeys.html

        Args:
            col (int): column
            row (int): row
            zoom (int): the zoom level

        Returns:
            str: quadkey

        Example:
            >>> # or checkout the unittest for this function
            >>> settings = {
                    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
                    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
                    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
                    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
                }
            >>> util = Utility(settings)
            >>> util.get_quadkeys(35210, 21493, 16)
            "1202102332221212"
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

    def get_map_tile_resource(self, location_data: tuple, location_type: str, zoom: int, img_size: int) -> str:
        """This function generates a url to get map_tile.

        For map_tile resource details, refer to
        https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/quick-start.html

        Args:
            location_data (tuple): either (latitude, longitude) or (column, row)
            location_type (str): either "latlon" or "colrow"
            zoom (int): the zoom level
            img_size (int): the image size. There are two options: 256 or 512

        Returns:
            str: the url for requesting a map tile resource

        Example:
            >>> # or checkout the unittest for this function
            >>> settings = {
                    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
                    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
                    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
                    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
                }
            >>> util = Utility(settings)
            >>> util.get_map_tile_resource((33.670156, -84.325984),"latlon", 14, 512)
            'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/14/4354/6562/512/png8?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw'
        """
        # if user did not provide a col, row, we use self.get_tile()
        if location_type == "latlon":
            (col, row) = self.get_tile(*location_data, zoom)
        elif location_type == "colrow":
            (col, row) = location_data

        total_url = self.map_tile_base_url + str(zoom) + '/' + str(int(col)) + '/' + str(int(
            row)) + '/' + str(img_size) + '/png8?app_id=' + self.app_id + '&app_code=' + self.app_code

        return total_url

    def get_traffic_json_resource(self, location_data: tuple, location_type: str, zoom: int) -> str:
        """This function generates a url to get traffic_json resource.

        For traffic_json resource details, refer to
        https://developer.here.com/rest-apis/documentation/traffic/topics/quick-start.html

        Args:
            location_data (tuple): either (latitude, longitude) or (column, row)
            location_type (str): either "latlon" or "colrow"
            zoom (int): the zoom level

        Returns:
            str: the url for requesting a traffic json resource

        Example:
            >>> # or checkout the unittest for this function
            >>> settings = {
                    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
                    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
                    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
                    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
                }
            >>> util = Utility(settings)
            >>> util.get_traffic_json_resource((34.9237, -82.4383), "latlon", 14)
            'https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&responseattributes=sh,fc'
        """
        if location_type == "latlon":
            (col, row) = self.get_tile(*location_data, zoom)
        elif location_type == "colrow":
            (col, row) = location_data

        quadkey = self.get_quadkeys(col, row, zoom)
        total_url = self.json_tile_base_url + 'app_id=' + self.app_id + \
            '&app_code=' + self.app_code + '&quadkey=' + quadkey + '&responseattributes=sh,fc'

        return total_url

    @staticmethod
    def produce_polygon(polygon_ordered_coordinates: List, zoom: int, plot_polygon: bool = False) -> Path:
        """This function use matplotlib.path to create a Path/polygon object. Later we can use
        this Path/polygon object to invoke Path.contains_point() method. For more details 
        on contains_point(), refer to 
        https://stackoverflow.com/questions/21328854/shapely-and-matplotlib-point-in-polygon-not-accurate-with-geolocation

        Args:
            polygon_ordered_coordinates (List): an ordered list of points that composes a polygon
            zoom (int): the zoom level
            plot_polygon (bool): If plot_polygon == True, we use matplotlib to plot the polygon

        Returns:
            matplotlib.path.Path: a Path polygon

        Example:
            >>> # or checkout the unittest for this function
            >>> example_polygon_ordered_coordinates = [[25.890099, -80.264561], [25.851873, -80.308744], [25.81123, -80.248538], [25.848596, -80.215765]]
        """
        polygon_tile_points = []
        for item in polygon_ordered_coordinates:
            polygon_tile_points += [Utility.get_tile(*item, zoom)]
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

    @staticmethod
    def get_area_tile_matrix(list_points: List, zoom: int, use_polygon: bool = False) -> pd.DataFrame:
        """This function takes the coordinates from list_points and calculate their tile (col, row),
        then it generate a matrix of tiles to cover the square area spanned by those coordinates. 
        If use_polygon == True, however, then we generate a polygon given by self.produce_polygon,
        and further eliminate any tiles in the matrix that are not **inside** of the polygon

        ::

            ###^^^^^^*####  (in this example, two coordinates are denoted as *
            #  ^^^^^^^   #   and this function should generate tile to cover the
            #  ^^^^^^^   #   area denoted by ^ and *)
            ###*^^^^^^####

        Args:
            list_points (List): list of GPS coordinates that you want to add
            zoom (int): the zoom level
            use_polygon (bool): If plot_polygon == True, then we generate a polygon given by self.produce_polygon,
                and further eliminate any tiles in the matrix that are not **inside** of the polygon

        Returns:
            DataFrame: a matrix filled with tiles number (col, row)

        Example:
            >>> # or checkout the unittest for this function
            >>> example_list_points = [(33.766764, -84.409533), (33.740003, -84.368978)]
        """
        tiles = []
        for point in list_points:
            tiles += [Utility.get_tile(*point, zoom)]
        left_col = min(tiles, key = lambda item: item[0])[0]
        right_col = max(tiles, key = lambda item: item[0])[0]
        top_row = min(tiles, key = lambda item: item[1])[1]
        bottom_row = max(tiles, key = lambda item: item[1])[1]  # notice bottom_row would actually have a higher number
        matrix = pd.DataFrame(index = range(bottom_row - top_row + 1), columns = range(right_col - left_col + 1))
        for row in range(len(matrix)):
            for col in range(len(matrix.iloc[0])):
                matrix.iloc[row,col] = (left_col + col, top_row + row)

        if use_polygon:
            polygon = Utility.produce_polygon(list_points, zoom, plot_polygon = False)
            for row in range(len(matrix)):
                for col in range(len(matrix.iloc[0])):
                    if matrix.iloc[row,col] in tiles:  # make sure the polygon points are covered
                        continue
                    if not polygon.contains_point(matrix.iloc[row,col]):
                        matrix.iloc[row,col] = None

        return matrix

    def get_area_tile_matrix_url(self, resource_type: str, list_points: List, zoom: int, use_polygon = False) -> pd.DataFrame:
        """This function takes the coordinates from list_points and calculate their tile (col, row),
        then it generate a matrix of tiles **URLs** (either map_tile urls or traffic_json urls)
        to cover the square area spanned by those coordinates.
        
        If use_polygon == True, however, then we generate a polygon given by self.produce_polygon,
        and further eliminate any tiles **URLs** in the matrix that are not **inside** of the polygon

        ::

            ###^^^^^^*####  (in this example, two coordinates are denoted as *
            #  ^^^^^^^   #   and this function should generate tile to cover the
            #  ^^^^^^^   #   area denoted by ^ and *)
            ###*^^^^^^####

        Args:
            resource_type (str): what types of *URLs* do you want, it can either be
                ``map_tile`` or ``traffic_json``
            list_points (List): list of GPS coordinates that you want to add
            zoom (int): the zoom level
            use_polygon (bool): If plot_polygon == True, then we generate a polygon given by self.produce_polygon,
                and further eliminate any tiles in the matrix that are not **inside** of the polygon

        Returns:
            DataFrame: a matrix filled with tiles number (col, row)

        Example:
            >>> # or checkout the unittest for this function
            >>> example_list_points = [(33.766764, -84.409533), (33.740003, -84.368978)]
        """
        matrix = self.get_area_tile_matrix(list_points, zoom, use_polygon)
        for row in range(len(matrix)):
            for col in range(len(matrix.iloc[0])):
                if matrix.iloc[row,col]:
                    if resource_type == "map_tile":
                        matrix.iloc[row,col] = self.get_map_tile_resource(location_data = matrix.iloc[row,col], location_type = "colrow", zoom = zoom, img_size = 512)
                    elif resource_type == "traffic_json":
                        matrix.iloc[row,col] = self.get_traffic_json_resource(location_data = matrix.iloc[row,col], location_type = "colrow", zoom = zoom)

        return matrix

    def register_route_tile(self, routing_info: Dict, zoom: int = 14) -> None:
        """This function takes routing_info generated by Google Direction API and
        store a ``route_collection.json`` in the your current directory (the directory
        that you used to run a file and call this function)

        Args:
            routing_info (Dict): The response document generated by Google Direction API
            zoom (int): the zoom level. Default is set to 14 because it is the 
                best level for meaningful details and it is also comparitively economical.

        Returns:
            None
        """

        ## first step, try to read colrow set if possible
        if os.path.isfile('route_collection.json'):
            with open('route_collection.json') as f:
                colrow_collection = json.load(f)
        else:
            colrow_collection = []

        ## second step, add all possible colrow in colrow_collection
        route = routing_info['routes'][0]
        leg = route['legs'][0]
        for step in leg['steps']:
            for path_item in step['path']:
                tile = self.get_tile(path_item['lat'], path_item['lng'], zoom)
                if tile not in colrow_collection:
                    colrow_collection += [tile]

        ## third step, save the route_set.json
        with open('route_collection.json', 'w') as f:
            json.dump(colrow_collection, f)
    
    def register_area_polygon(self, area_description: str, geojson_polygon: str) -> None:
        """

        Args:
            routing_info (Dict): 

        Returns:
            None
        """

        ## first step, try to read colrow set if possible
        if os.path.isfile('area_collection.json'):
            with open('area_collection.json') as f:
                area_collection = json.load(f)
        else:
            area_collection = []

        ## second step, add all possible colrow in colrow_collection
        area_collection += [{
            'area_description': area_description,
            'polygon': self.read_geojson_polygon(geojson_polygon)
        }]

        ## third step, save the route_set.json
        with open('area_collection.json', 'w') as f:
            json.dump(area_collection, f)

    def get_route_tile_matrix_url(self) -> pd.DataFrame:
        """This function load the ``route_collection.json`` in the your current directory
        and return a traffic_json url matrix

        Args:
            None 

        Returns:
            DataFrame: a traffic_json url matrix that we can use to crawl data
        """

        if os.path.isfile('route_collection.json'):
            with open('route_collection.json') as f:
                colrow_collection = json.load(f)
        else:
            raise Exception('route_collection.json does not exist, try using server.util.register_route_tile_matrix_url()') 
        ## last step, return a pandas matrix
        matrix = pd.DataFrame(index = range(1), columns = range(len(colrow_collection)))
        i = 0
        for item in colrow_collection:
            matrix.iloc[0,i] = self.get_traffic_json_resource(location_data = item, location_type = "colrow", zoom = 14)
            i += 1

        return matrix

    def get_area_polygon_collection(self) -> List:
        """

        Args:
            routing_info (Dict): 

        Returns:
            None
        """

        ## first step, try to read colrow set if possible
        if os.path.isfile('area_collection.json'):
            with open('area_collection.json') as f:
                area_collection = json.load(f)
            return area_collection
        else:
            raise Exception('area_collection.json does not exist, try using server.util.register_area_polygon()')


    def assemble_matrix_images(self, matrix: pd.DataFrame) -> pd.DataFrame:
        """This function load a map_tile url matrix and assemble it as a 
        image matrix. Also it will print out a image for you to see.

        Args:
            matrix (pd.DataFrame): a map_tile url matrix

        Returns:
            DataFrame: matrix of images
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

    @staticmethod
    def get_distance(point1: tuple, point2: tuple, location_type: str = "latlon", distance_formula: str = "great_circle", unit:str = "meters") -> float:
        """This function returns the distance between point1 and poin2 in meters.

        Note:
            this function is a quick wraper for geopy.

        Args:
            point1 (tuple): a GPS coordinates
            point2 (tuple): a GPS coordinates
            location_type (str): "latlon" meaning the format is (latitude, longitude)
                for ``point1`` and ``point2``
            distance_formula (str): two options for distance formula, either
                ``'great_circle'`` or ``'vincenty'``
            unit (str): "meters"

        Returns:
            float: distance between point1 and point2
        """
        if distance_formula == "great_circle":
            return great_circle(point1, point2).meters
        elif distance_formula == "vincenty":
            return vincenty(point1, point2).meters
        else:
            raise Exception('undefined distance_formula')

    @staticmethod
    def read_geojson_polygon(geojson_polygon: str) -> List:
        """Given a polygon in geojson string format,
        this function outputs a polygon list that consist of coordiantes
        that has [latitude, longitude] format.

        Args:
            geojson_polygon (str): a polygon of geojson encoding. 

        Returns:
            List: a list that consist of coordiantesthat has 
            [latitude, longitude] format

        Example:
            >>> checkout the unittest for this function
            >>> geojson_polygon = '''
            {
              "type": "FeatureCollection",
              "features": [
                {
                  "type": "Feature",
                  "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                      [
                        [
                          -84.38658714294434,
                          33.76908761144743
                        ],
                        [
                          -84.37294006347656,
                          33.766590334877485
                        ]
                      ]
                    ]
                  },
                  "properties": {}
                }
              ]
           '''  # notice this should be a string
            >>> settings = {
                    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
                    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
                    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
                    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
                }
            >>> util = Utility(settings)
            >>> util.read_geojson_polygon(geojson_polygon)
            [[33.76908761144743, -84.38658714294434],
            [33.766590334877485, -84.37294006347656]]

        """
        geojson_polygon_dict = json.loads(geojson_polygon)
        polygon_coordinates = geojson_polygon_dict['features'][0]['geometry']['coordinates'][0]
        polygon = []
        for item in polygon_coordinates:
            polygon += [[item[1], item[0]]]
        return polygon

    @staticmethod
    def matrix_coverage(matrix: pd.DataFrame):
        """Generate some statistical information about
        how many valid query tiles are there in your
        provided matrix

        Args:
            matrix (pd.DataFrame): The JSON raw data

        Returns:
            None, but it prints out some information
            about your matrix
        """
        filled_count = 0
        None_count = 0
        for row in range(len(matrix)):
            for col in range(len(matrix.iloc[0])):
                if matrix.iloc[row, col]:
                    filled_count += 1
                else:
                    None_count += 1

        print('matrix has a total of', len(matrix) *len(matrix.iloc[0]), 'tiles')
        print(filled_count, 'of them are filled')
        print(None_count, 'of them are None because of the polygon limitation')
