import rethinkdb as r
from typing import Dict, List
import copy
import requests
from dateutil import parser
import datetime
import pandas as pd
import time
import json

class TrafficData:

    def __init__(self):
        """
        This class establishes a connection towards the database
        """
        self.conn = r.connect('localhost', 28015)
        self.latest_crawled_batch_id = r.db('Traffic').table('crawled_batch').order_by(index = r.desc("crawled_timestamp")).limit(1).run(self.conn).next()['id']

    def insert_json_data(self, data: Dict, crawled_batch_id: str = None) -> None:
        """
        inputs: data: Dict(json dictionary)

        The function ...

        For documentation of the file format, refer to
        http://traffic.cit.api.here.com/traffic/6.0/xsd/flow.xsd?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw

        return: None
        """
        ## insert the data into original_data table
        created_timestamp = parser.parse(data['CREATED_TIMESTAMP'])
        data['CREATED_TIMESTAMP'] = r.expr(created_timestamp).run(self.conn)
        if crawled_batch_id:
            data['crawled_batch_id'] = crawled_batch_id
        insert_result = r.db('Traffic').table('original_data').insert(data).run(self.conn)
        original_data_id = insert_result['generated_keys'][0]

        ## start parsing the data
        for RWS_item in data['RWS']:
            for RW_item in RWS_item['RW']:
                for FIS_item in RW_item['FIS']:
                    for FI_item in FIS_item['FI']:
                        # our CUSTOM attributes, record
                        # parent_DE: parent location description
                        # original_data_id: the original json document that we have downloaded
                        FI_item['CUSTOM'] = {
                            'parent_DE': RW_item['DE'],
                            'original_data_id': original_data_id,
                            'created_timestamp': r.expr(created_timestamp).run(self.conn),
                            'crawled_batch_id': crawled_batch_id
                        }
                        SHP_list = copy.deepcopy(FI_item['SHP'])
                        FI_item['SHP'] = "See table road_data"
                        insert_result = r.db('Traffic').table('flow_data').insert(FI_item).run(self.conn)
                        flow_data_id = insert_result['generated_keys'][0]
                        
                        for SHP_item in SHP_list:
                            SHP_item['flow_data_id'] = flow_data_id
                            try:
                                SHP_item['geometry'] = r.line(r.args(self.parse_SHP_values(SHP_item['value']))).run(self.conn)
                                SHP_item['created_timestamp'] = r.expr(created_timestamp).run(self.conn)
                                SHP_item['crawled_batch_id'] = crawled_batch_id
                                r.db('Traffic').table('road_data').insert(SHP_item).run(self.conn)
                            except:
                                print('exception in parsing SHP values')
                                raise

    def parse_SHP_values(self, value: List) -> List:
        """
        inputs: value: List(the ['SHP']['values'])
        example inputs:
        ["34.9495,-82.43912 34.94999,-82.4392 34.95139,-82.4394 "], where each point is 

        This function convert the values into a list that conforms line specification of RethinkDB.
        More specifically, in RethinkDB every point has the **opposite** parameters: (long, lat) while our 
        data has point (lat, long). For more details,
        refer to https://rethinkdb.com/api/python/line/ and https://rethinkdb.com/api/javascript/point/

        example outputs:
        [[-82.43912, 34.9495], [-82.4392, 34.94999], [-82.4394, 34.95139]]
        """
        temp = value[0].split()
        result = []
        for item in temp:
            item = item.split(',')
            item = [float(i) for i in item]
             # we need to reverse the [lat, long] to [long, lat] to comply with
             # RethinkDB specifications at https://rethinkdb.com/api/javascript/point/
            item.reverse()
            result += [item]

        return result
    
    def read_traffic_data(self, url: str) -> Dict:
        """
        inputs: url: str(a url that has HERE traffic json file)
        example inputs: https://traffic.cit.api.here.com/traffic/6.2/flow.json?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw&quadkey=03200303033202&responseattributes=sh,fc 

        This functios takes the input url and return its json object

        return :Dict(json dict)
        """
        r = requests.get(url)
        return r.json()

    def helper_create_tables(self):
        """
        This is a helper function to create tables in rethinkDB
        """
        ## creating tables
        r.db('Traffic').table_create('original_data').run(self.conn)
        r.db('Traffic').table_create('road_data').run(self.conn)
        r.db('Traffic').table_create('flow_data').run(self.conn)
        r.db('Traffic').table_create('crawled_batch').run(self.conn)

        ## creating index
        r.db('Traffic').table('original_data').index_create('crawled_batch_id').run(self.conn)
        r.db('Traffic').table('flow_data').index_create('crawled_batch_id', r.row["CUSTOM"]["crawled_batch_id"]).run(self.conn)
        r.db('Traffic').table('flow_data').index_create('original_data_id', r.row["CUSTOM"]["original_data_id"]).run(self.conn)
        r.db('Traffic').table('road_data').index_create('flow_data_id').run(self.conn)
        r.db('Traffic').table('road_data').index_create('geometry', geo=True).run(self.conn)
        r.db('Traffic').table('road_data').index_create('crawled_batch_id').run(self.conn)
        r.db('Traffic').table('crawled_batch').index_create('crawled_timestamp').run(self.conn)

        ## depreciated index
        #r.db('Traffic').table('flow_data').index_create('created_timestamp', r.row["CUSTOM"]["created_timestamp"]).run(self.conn)
        #r.db('Traffic').table('road_data').index_create('created_timestamp').run(self.conn)

    def store_matrix_json(self, matrix_list: List) -> None:
        """
        inputs: matrix: pd.DataFrame(a matrix of urls of json traffic information generated by ultil.get_area_tile_matrix_url())
        example inputs:
                                                           0  \
        0  https://traffic.cit.api.here.com/traffic/6.2/f...   
        1  https://traffic.cit.api.here.com/traffic/6.2/f...   
        2  https://traffic.cit.api.here.com/traffic/6.2/f...   

                                                           1  \
        0  https://traffic.cit.api.here.com/traffic/6.2/f...   
        1  https://traffic.cit.api.here.com/traffic/6.2/f...   
        2  https://traffic.cit.api.here.com/traffic/6.2/f...   

                                                           2  
        0  https://traffic.cit.api.here.com/traffic/6.2/f...  
        1  https://traffic.cit.api.here.com/traffic/6.2/f...  
        2  https://traffic.cit.api.here.com/traffic/6.2/f...  

        This function takes the matrix, download all the jsons in the matrix, store them in 
        the database
        """
        # store info about matrix_list and when do we crawled them
        if len(matrix_list) == 0:
            print('matrix_list has no element')
            return
        crawled_epochtime = time.time()
        storing_dict = {}
        storing_dict['crawled_timestamp'] =  r.epoch_time(time.time()).run(self.conn)
        matrix_list_encoding = []
        for matrix in matrix_list:
            matrix_list_encoding += [json.loads(matrix.to_json(orient='table'))]
        storing_dict['crawled_matrix_encoding'] = matrix_list_encoding
        # notice you can reverse the encoding, refer to 
        # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
        insert_result = r.db('Traffic').table('crawled_batch').insert(storing_dict).run(self.conn)
        crawled_batch_id = insert_result['generated_keys'][0]

        # start inserting actual data
        for matrix in matrix_list:
            for i in range(len(matrix)):
                for j in range(len(matrix.loc[0])):
                    traffic_data = self.read_traffic_data(matrix.loc[i, j])
                    self.insert_json_data(traffic_data, crawled_batch_id)

    def fetch_geojson_item(self, road_data_id: str, calculate_traffic_color = True) -> Dict:
        """
        inputs: road_data_id: str(a primary key of road_data table), calculate_traffic_color = True

        Notice the road_data table only stores the 'geometry' info of a geojson object.
        An example data from road_data would be 

        {
            "$reql_type$":  "GEOMETRY" ,
            "coordinates": [
                [
                    -82.42968 ,
                    34.92954
                ] ,
                [
                    -82.43003 ,
                    34.92729
                ]
            ] ,
            "type":  "LineString"
        } ,

        This function uses a road_data_id(primary key) to fethe a geojson object from 
        the road_data database. If calculate_traffic_color == True, then we also use
        traffic_flow_color_scheme() to calcuroad_data_idlate a color for the road

        Example output with color is :
        {
            "type": "Feature",
            "geometry": {
                "coordinates": [
                    [
                        -82.42907,
                        34.91623
                    ],
                    [
                        -82.42911,
                        34.91647
                    ],
                    [
                        -82.42917,
                        34.91684
                    ]
                ],
                "type": "LineString"
            },
            "properties": {
                "TMC": {
                    "DE": "Old Buncombe Rd",
                    "LE": 1.67396,
                    "PC": 10934,
                    "QD": "-"
                },
                "CF": {
                    "CN": 0.7,
                    "FF": 42.25,
                    "JF": 1.71568,
                    "LN": [],
                    "SP": 33.55,
                    "SU": 33.55,
                    "TY": "TR"
                },
                "color": "green"
            }
        }

        For more infomation about geojson, check out
        http://geojson.org/
        """
        data = r.db('Traffic').table('road_data').get(road_data_id).run(self.conn)
        flow_data_id = data['flow_data_id']
        flow_data = r.db('Traffic').table('flow_data').get(flow_data_id).run(self.conn)
        geojson_properties = {'TMC': flow_data['TMC'], 'CF': flow_data['CF'][0]}
        
        # possibly we need to calculate traffic color for the road
        if calculate_traffic_color:
            geojson_properties['color'] = self.traffic_flow_color_scheme(geojson_properties['CF'])

        geojson_geometry = r.db('Traffic').table('road_data').get(road_data_id)['geometry'].to_geojson().run(self.conn)
        geojson_type = "Feature"

        return {"type": geojson_type, "geometry": geojson_geometry, "properties": geojson_properties}

    @staticmethod
    def generate_geojson_collection(geojson_list: List) -> Dict:
        """
        inputs: geojson_list: List (a list of geojson objects)
        example inputs:
        [ {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [125.6, 10.1]
          },
          "properties": {
            "name": "Dinagat Islands"
          }
        }, ....]

        This function takes a list of geojson objects and assemble them in the following way
        The following format allows for multiple geojson object to be stored in the 
        same geojson object. For more details, refer to 
        https://macwright.org/2015/03/23/geojson-second-bite.html

        Example outputs:
        {
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [125.6, 10.1]
              },
              "properties": {
                "name": "Dinagat island"
              }
            },
            {
              "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [15,15]
              },
              "properties": {
                "name": "Test Islands"
              }
            }
          ]
        }

        such that the output is still a geojson_object but it contains all the 
        geojson_object in geojson_list
        """
        output_geojson = {"type": "FeatureCollection"}
        output_geojson['features'] = geojson_list
        return output_geojson

    def traffic_flow_color_scheme(self, traffic_flow_data: Dict) -> str: 
        """
        inputs: traffic_flow_data: Dict (traffic flow data)
        example inputs:
        {
            "CN": 0.7 ,  // Confidence, an indication of how the speed was determined. -1.0 road closed. 1.0=100% 0.7-100% Historical Usually a value between .7 and 1.0.
            "FF": 41.01 , // The free flow speed on this stretch of road.
            "JF": 1.89393 , // The number between 0.0 and 10.0 indicating the expected quality of travel. When there is a road closure, the Jam Factor will be 10. As the number approaches 10.0 the quality of travel is getting worse. -1.0 indicates that a Jam Factor could not be calculated.
            "LN": [ ],
            "SP": 31.69 , // Speed (based on UNITS) capped by speed limit MPH
            "SU": 31.69 , // Speed (based on UNITS) not capped by speed limit
            "TY":  "TR"   //Used when it is needed to differentiate between different kinds of location types.
        }
        for further details on those encoding, refer to 
        http://traffic.cit.api.here.com/traffic/6.0/xsd/flow.xsd?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw

        Given the traffic_flow_data, we calculate a color that indicates the traffic situation of the road

        return :str(a color)
        """
        
        ## right now we just simply write a temporary fix
        if traffic_flow_data['JF'] < 3:
            return 'green'  # #55ce37 it also has hash value color support
        elif traffic_flow_data['JF'] >= 3 and traffic_flow_data['JF'] <= 6:
            return 'yellow'
        else:
            return 'red'

    def display_json_traffic(self, original_data_id_list: List) -> Dict:
        """
        inputs: original_data_id: str(the primary key/id for original_data table)
        ## TODO: apparently a lot more optimization can be done here
        ## TODO: there might be overlapping documents with the same road_data_id

        This function takes a list of original_data_id, get every road related to them
        and lastly output a geojson object containing every road.

        """
        geojson_list = []
        for original_data_id in original_data_id_list:
            ## maybe instead of query the whole document, we just query the index?
            flow_data_collection = r.db("Traffic").table("flow_data").get_all(original_data_id, index="original_data_id").run(self.conn)  
            for flow_data in flow_data_collection:
                flow_data_id = flow_data['id']
                road_data_collection = r.db("Traffic").table("road_data").get_all(flow_data_id, index="flow_data_id").run(self.conn)

                for road_data in road_data_collection:
                    geojson_list += [self.fetch_geojson_item(road_data['id'])]

        ## Lastly we assemble the geojson_list by using generate_geojson_collection()
        return TrafficData.generate_geojson_collection(geojson_list)

    def get_nearest_road(self, location_data: tuple, max_dist: int, max_results: int = 1, crawled_batch_id: int = None, location_type: str = "latlon") -> Dict:
        """
        inputs: location_data: tuple, max_dist: int, max_results: int, location_type: str, 
        crawled_batch_id: int(it indicate which crawled patch you want to query)

        The location_type and corresponding location data is as follow
        location_type = "latlon"; location_data = (latitude, longitude)  
        we currently only support latlon

        example outputs:
        {'dist': 2.5938097681046823,
         'doc': {'FC': 4,
          'created_timestamp': datetime.datetime(2017, 6, 14, 20, 11, 40, tzinfo=<rethinkdb.ast.RqlTzinfo object at 0x000001817771C518>),
          'flow_data_id': '741f5e08-29cc-4a35-a7fa-80e8286a3f21',
          'geometry': {'$reql_type$': 'GEOMETRY',
           'coordinates': [[-84.39459, 33.73684], [-84.39548, 33.73686]],
           'type': 'LineString'},
          'id': '85179647-1e04-4306-ad5f-5054dadedd0b',
          'value': ['33.73684,-84.39459 33.73686,-84.39548 ']}
        }

        """
        if not crawled_batch_id:
            crawled_batch_id = self.latest_crawled_batch_id
        query_result = r.db('Traffic').table('road_data').get_nearest(r.point(location_data[1],location_data[0]), index = 'geometry', 
                                                                max_dist = max_dist, max_results = max_results).filter(
                                                                lambda user: user["doc"]["crawled_batch_id"] == crawled_batch_id).run(self.conn)  # Probably not very efficient

        if len(query_result) == 0:
            raise Exception('query_result has no results')
        else:
            return query_result[0]


    def get_historic_traffic(self, routing_info: Dict, crawled_batch_id: int = None):
        """
        ## TODO: inplement historic collection 
        inputs: route_info: Dict(a json object that contains routing information),
        historic_collection_quantity: int(how many historic collection do you want)
        crawled_batch_id: int(it indicate which crawled patch you want to query)
        Example input: see google_routing.json

        """
        if not crawled_batch_id:
            crawled_batch_id = self.latest_crawled_batch_id
        ## there might be multiple **routes**, but we just worry about one for now
        route = routing_info['routes'][0]
        ## there might be multiple **legs**, but we just worry about one for now
        leg = route['legs'][0]

        ## we don't want duplicate road in our collection
        road_id_collection = {}
        duplicate_road_id = []
        geojson_road_list = []

        for step in leg['steps']:
            for path_item in step['path']:
                try:
                    road_document = self.get_nearest_road((path_item['lat'], path_item['lng']), max_dist = 1000, crawled_batch_id = crawled_batch_id)
                    road_data_id = road_document['doc']['id']
                except:
                    continue

                ## see if road_data_id already exists in our collection
                if road_data_id not in road_id_collection:
                    road_id_collection[road_data_id] = True
                    geojson_road_list += [self.fetch_geojson_item(road_data_id)]
                else:
                    duplicate_road_id += [road_data_id]

        print('there are', len(duplicate_road_id), 'many duplicate road element')
        print(road_id_collection)

        return TrafficData.generate_geojson_collection(geojson_road_list)


    def get_historic_batch(self):
        """

        example output:
        [{'crawled_timestamp': '2017-06-19T19:29:37.845000+00:00',
          'id': 'a6f344c6-9941-41b4-aaf7-83e6ecab5ec2'},
         {'crawled_timestamp': '2017-06-19T17:36:56.453000+00:00',
          'id': '3872cf48-e40d-4826-86aa-bc8ee1b36631'},
         {'crawled_timestamp': '2017-06-19T17:20:00.645000+00:00',
          'id': 'fbbc23d5-5bcb-4c99-af12-6b66022effcd'}]
        """
        query_result = r.db('Traffic').table('crawled_batch').order_by(index = r.desc('crawled_timestamp')).limit(10).run(self.conn)
        batch_list = []
        for batch_item in query_result:
            batch_item.pop('crawled_matrix_encoding', None)
            batch_item['crawled_timestamp'] = batch_item['crawled_timestamp'].isoformat()
            batch_list += [batch_item]

        return batch_list

