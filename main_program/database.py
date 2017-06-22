import rethinkdb as r
from typing import Dict, List
import copy
import requests
from dateutil import parser
import datetime
import pandas as pd
import time
import json
import asyncio
import threading


class TrafficData:

    def __init__(self, database_name: str = "Traffic", connection = None):
        """
        This class establishes a connection towards the database
        """
        self.conn = r.connect('localhost', 28015)
        if database_name in r.db_list().run(self.conn):
            self.conn.use(database_name)
        else:
            self.db_create(database_name).run(self.conn)
            self.conn.use(database_name)
        self.latest_crawled_batch_id = r.table('crawled_batch').order_by(index = r.desc("crawled_timestamp")).limit(1).run(self.conn).next()['id']

    def insert_json_data(self, data: Dict, crawled_batch_id: str = None, testing = False) -> None:
        """
        inputs: data: Dict(json dictionary)

        The function ...

        We will try to avoid duplicate of flow_data document and road_data document

        For documentation of the file format, refer to
        http://traffic.cit.api.here.com/traffic/6.0/xsd/flow.xsd?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw

        return: None, although if testing = True, we would return a tuple (original_data_insertion_ids, flow_data_insertion_ids, road_data_insertion_ids)
        to trace what have we inserted
        """
        ## Testing purpose
        if testing:  
            # Notice you can ignore every lines under if testing:
            # codes under that block are for testing purposes
            # It's not really part of the core code
            flow_data_duplicate = 0
            road_data_duplicate = 0
            original_data_insertion_ids = []
            flow_data_insertion_ids = []
            road_data_insertion_ids = []

        if not data:
            print('inserted nothing')
            return None

        ## insert the data into original_data table
        created_timestamp = parser.parse(data['CREATED_TIMESTAMP'])
        data['CREATED_TIMESTAMP'] = r.expr(created_timestamp).run(self.conn)
        if crawled_batch_id:
            data['crawled_batch_id'] = crawled_batch_id
        insert_result = r.table('original_data').insert(data).run(self.conn)
        original_data_id = insert_result['generated_keys'][0]
        if testing:
            original_data_insertion_ids += [original_data_id]

        ## start parsing the data
        for RWS_item in data['RWS']:
            for RW_item in RWS_item['RW']:
                for FIS_item in RW_item['FIS']:
                    for FI_item in FIS_item['FI']:
                        SHP_list = copy.deepcopy(FI_item['SHP'])
                        CF_item = FI_item['CF'][0]
                        CF_item['original_data_id'] = original_data_id
                        CF_item['created_timestamp'] = r.expr(created_timestamp).run(self.conn)
                        CF_item['crawled_batch_id'] = crawled_batch_id

                        ## we check if the flow_data alerady exist
                        TMC_encoding = json.dumps(FI_item['TMC'], sort_keys = True)  ## sort the key to elimincate different encoding of the same python Dict
                        flow_data_doc = r.table('flow_data').get(TMC_encoding).run(self.conn)

                        ## flow_data = None means the flow_data_doc does *not* exists
                        if not flow_data_doc:
                            flow_data_insertion = {}
                            flow_data_insertion["id"]  = TMC_encoding
                            flow_data_insertion["CF"] = {crawled_batch_id: [CF_item]}
                            flow_data_insertion["TMC"] = FI_item['TMC']
                            flow_data_insertion['SHP'] = "See table road_data"
                            r.table('flow_data').insert(flow_data_insertion).run(self.conn)
                            flow_data_id = TMC_encoding
                            if testing:
                                flow_data_insertion_ids += [TMC_encoding]

                        ## if flow_data_doc already exist, we simply update the CF field
                        else: 
                            if testing: 
                                flow_data_duplicate += 1  
                            if crawled_batch_id in flow_data_doc['CF']:
                                flow_data_doc['CF'][crawled_batch_id] = [CF_item] + flow_data_doc['CF'][crawled_batch_id]
                            else:
                                flow_data_doc['CF'][crawled_batch_id] = [CF_item]
                            flow_data_id = flow_data_doc['id'] 
                            r.table('flow_data').get(TMC_encoding).update({"CF": flow_data_doc['CF']}).run(self.conn)
                        
                        for SHP_item in SHP_list:
                            geometry_encoding = json.dumps(SHP_item['value'], sort_keys = True)[:120]  # primary key's length is at most 127
                            road_data_doc = r.table('road_data').get(geometry_encoding).run(self.conn)

                            # if road_data_doc does not exist, we insert the road into db. Notice that if road_data_doc exists, we simply ignore it.
                            if not road_data_doc:
                                SHP_item['flow_data_id'] = flow_data_id
                                try:
                                    SHP_item['geometry'] = r.line(r.args(self.parse_SHP_values(SHP_item['value']))).run(self.conn)
                                    SHP_item['id'] = geometry_encoding
                                    r.table('road_data').insert(SHP_item).run(self.conn)
                                    if testing:
                                        road_data_insertion_ids += [geometry_encoding]
                                except:
                                    raise Exception('exception in parsing SHP values')
                            else:
                                # maybe have different flow_data_id????
                                if testing:
                                    road_data_duplicate += 1
                                    ## Notice it is possible for a road to point to different flow_data_id
                                    ## comment out the following code to see what I mean.
                                    # if road_data_doc['flow_data_id'] != flow_data_id:
                                    #     print("======================")
                                    #     print(road_data_doc['flow_data_id'])
                                    #     print(flow_data_id)

        if testing:
            print('there are ',flow_data_duplicate, 'flow_data duplicate')
            print('there are ',road_data_duplicate, 'road_data duplicate')
            return (original_data_insertion_ids, flow_data_insertion_ids, road_data_insertion_ids)


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
        if r.status_code == 204:  # no content
            return None
        return r.json()

    def helper_create_tables(self):
        """
        This is a helper function to create tables in rethinkDB
        """
        ## creating tables
        r.table_create('original_data').run(self.conn)
        r.table_create('road_data').run(self.conn)
        r.table_create('flow_data').run(self.conn)
        r.table_create('crawled_batch').run(self.conn)

        ## creating index
        r.table('original_data').index_create('crawled_batch_id').run(self.conn)
        #r.table('flow_data').index_create('crawled_batch_id', r.row["CUSTOM"]["crawled_batch_id"]).run(self.conn)
        #r.table('flow_data').index_create('original_data_id', r.row["CUSTOM"]["original_data_id"]).run(self.conn)
        r.table('road_data').index_create('flow_data_id').run(self.conn)
        r.table('road_data').index_create('geometry', geo=True).run(self.conn)
        r.table('road_data').index_create('crawled_batch_id').run(self.conn)
        r.table('crawled_batch').index_create('crawled_timestamp').run(self.conn)

        ## depreciated index
        #r.table('flow_data').index_create('created_timestamp', r.row["CUSTOM"]["created_timestamp"]).run(self.conn)
        #r.table('road_data').index_create('created_timestamp').run(self.conn)

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
        insert_result = r.table('crawled_batch').insert(storing_dict).run(self.conn)
        crawled_batch_id = insert_result['generated_keys'][0]

        # start inserting actual data
        for matrix in matrix_list:
            for i in range(len(matrix)):
                for j in range(len(matrix.loc[0])):
                    traffic_data = self.read_traffic_data(matrix.loc[i, j])
                    self.insert_json_data(traffic_data, crawled_batch_id)

    def fetch_geojson_item(self, road_data_id: str, crawled_batch_id: str = None, calculate_traffic_color = True) -> Dict:
        """
        inputs: road_data_id: str(a primary key of road_data table), calculate_traffic_color = True

        Notice the road_data table only stores the 'geometry' info of a geojson object.
        An example data from road_data would be 

        {
          "FC": 2,
          "flow_data_id": "{\"DE\": \"University Ave/Exit 244\", \"LE\": 1.57367, \"PC\": 4117, \"QD\": \"-\"}",
          "geometry": {
            "$reql_type$": "GEOMETRY",
            "coordinates": [
              [
                -84.40353,
                33.70524
              ],
              [
                -84.40347,
                33.70551
              ],
              [
                -84.40335,
                33.70597
              ]
            ],
            "type": "LineString"
          },
          "id": "[\"33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 \"]",
          "value": [
            "33.70524,-84.40353 33.70551,-84.40347 33.70597,-84.40335 "
          ]
        },

        This function uses a road_data_id(primary key) to fethe a geojson object from 
        the road_data database. If calculate_traffic_color == True, then we also use
        traffic_flow_color_scheme() to calcuroad_data_idlate a color for the road

        Example output with color is :
        {
          "geometry": {
            "coordinates": [
              [
                -84.40353,
                33.70524
              ],
              [
                -84.40347,
                33.70551
              ],
              [
                -84.40335,
                33.70597
              ]
            ],
            "type": "LineString"
          },
          "properties": {
            "CF": {
              "CN": 0.99,
              "FF": 55.3,
              "JF": 8.73969,
              "LN": [],
              "SP": 12.26,
              "SU": 12.26,
              "TY": "TR",
              "crawled_batch_id": "6dcfea39-e0e0-47e5-b8cc-2d20e1acbd46",
              "created_timestamp": "2017-06-20T19:05:33+00:00",
              "original_data_id": "8b8c9c9a-afbb-41dd-8e65-9111c38d3cb8"
            },
            "TMC": {
              "DE": "University Ave/Exit 244",
              "LE": 1.57367,
              "PC": 4117,
              "QD": "-"
            },
            "color": "red"
          },
          "type": "Feature"
        }

        For more infomation about geojson, check out
        http://geojson.org/
        """
        if not crawled_batch_id:
            crawled_batch_id = self.latest_crawled_batch_id
        data = r.table('road_data').get(road_data_id).run(self.conn)
        flow_data_id = data['flow_data_id']
        flow_data = r.table('flow_data').get(flow_data_id).run(self.conn)
        flow_data['CF'][crawled_batch_id][0]['created_timestamp'] = flow_data['CF'][crawled_batch_id][0]['created_timestamp'].isoformat()
        geojson_properties = {'TMC': flow_data['TMC'], 'CF': flow_data['CF'][crawled_batch_id][0]}
        
        # possibly we need to calculate traffic color for the road
        if calculate_traffic_color:
            geojson_properties['color'] = self.traffic_flow_color_scheme(geojson_properties['CF'])

        geojson_geometry = r.table('road_data').get(road_data_id)['geometry'].to_geojson().run(self.conn)
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
        Check out the following link for coloring Map
        https://developer.here.com/rest-apis/documentation/traffic/topics/tiles.html

        return :str(a color)
        """
        
        ## right now we just simply write a temporary fix
        if traffic_flow_data['JF'] < 4:
            return 'green'  # #55ce37 it also has hash value color support
        elif traffic_flow_data['JF'] >= 4 and traffic_flow_data['JF'] < 8:
            return 'yellow'
        elif traffic_flow_data['JF'] >= 8 and traffic_flow_data['JF'] < 10:
            return 'red'
        else:
            return 'black'

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

    def get_nearest_road(self, location_data: tuple, max_dist: int, max_results: int = 1, location_type: str = "latlon") -> Dict:
        """
        inputs: location_data: tuple, max_dist: int, max_results: int, location_type: str, 
        crawled_batch_id: int(it indicate which crawled patch you want to query)

        The location_type and corresponding location data is as follow
        location_type = "latlon"; location_data = (latitude, longitude)  
        we currently only support latlon

        example outputs:
        {
          "dist": 11.523928527983454,
          "doc": {
            "FC": 4,
            "flow_data_id": "{\"DE\": \"US-278/US-29/Ponce De Leon Ave NE\", \"LE\": 0.58406, \"PC\": 12873, \"QD\": \"-\"}",
            "geometry": {
              "$reql_type$": "GEOMETRY",
              "coordinates": [
                [
                  -84.37777,
                  33.76865
                ],
                [
                  -84.37775,
                  33.76952
                ],
                [
                  -84.37774,
                  33.76994
                ]
              ],
              "type": "LineString"
            },
            "id": "[\"33.76865,-84.37777 33.76952,-84.37775 33.76994,-84.37774 \"]",
            "value": [
              "33.76865,-84.37777 33.76952,-84.37775 33.76994,-84.37774 "
            ]
          }
        }
        """
        query_result = r.table('road_data').get_nearest(r.point(location_data[1],location_data[0]), index = 'geometry', 
                                                                max_dist = max_dist, max_results = max_results).run(self.conn)  # Probably not very efficient

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
                    road_document = self.get_nearest_road((path_item['lat'], path_item['lng']), max_dist = 1000)
                    road_data_id = road_document['doc']['id']
                except:
                    print('cant find nearest road once')

                ## see if road_data_id already exists in our collection
                if road_data_id not in road_id_collection:
                    road_id_collection[road_data_id] = True
                    geojson_road_list += [self.fetch_geojson_item(road_data_id, crawled_batch_id = crawled_batch_id)]
                else:
                    duplicate_road_id += [road_data_id]

        print('there are', len(duplicate_road_id), 'many duplicate road element')
        #print(road_id_collection)

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
        query_result = r.table('crawled_batch').order_by(index = r.desc('crawled_timestamp')).limit(10).run(self.conn)
        batch_list = []
        for batch_item in query_result:
            batch_item.pop('crawled_matrix_encoding', None)
            batch_item['crawled_timestamp'] = batch_item['crawled_timestamp'].isoformat()
            batch_list += [batch_item]

        return batch_list