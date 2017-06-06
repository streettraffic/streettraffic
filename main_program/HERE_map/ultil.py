import math


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
    xTile = n * ((lon + 180) / 360)  # Column
    yTile = n * (1 - (math.log(math.tan(lat_rad) + 1 /
                               math.cos(lat_rad)) / math.pi)) / 2  # Row

    return (xTile, yTile)


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
        print(mask)
        if (col & mask) != 0:  # notice this is a bitwise operator!! different from && or and
            digit += 1
        if (row & mask) != 0:
            digit += 2
        quadkey += str(digit)

        print(digit, quadkey)

    return quadkey

# todo: convert quadkeys to tile
# todo: convert tile to coordinates
