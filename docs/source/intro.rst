An Introduction to StreetTraffic's
=========================================

Let's start a hello world:: 

    ## import system module
    import json
    import rethinkdb as r
    import time
    import datetime as dt
    import asyncio

    ## import custom module
    from streettraffic.server import TrafficServer
    from streettraffic.predefined.cities import San_Francisco_polygon

    settings = {
        'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
        'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
        'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
        'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
    }


    ## initialize traffic server
    server = TrafficServer(settings)
    San_Francisco_matrix = server.util.get_area_tile_matrix_url("traffic_json", San_Francisco_polygon, 14, True)
    server.traffic_matrix_list = [San_Francisco_matrix]

    server.start()
    conn = server.traffic_data.conn
