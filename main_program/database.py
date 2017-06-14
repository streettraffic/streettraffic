import rethinkdb as r
from typing import Dict, List
import copy
import requests
from dateutil import parser
import datetime
import pandas as pd

class TrafficData:

    def __init__(self):
        r.connect('localhost', 28015).repl()

    def insert_json_data(self, data: Dict) -> None:
        """
        inputs: data: Dict(json dictionary)

        The function ...

        For documentation of the file format, refer to
        http://traffic.cit.api.here.com/traffic/6.0/xsd/flow.xsd?app_id=F8aPRXcW3MmyUvQ8Z3J9&app_code=IVp1_zoGHdLdz0GvD_Eqsw

        return: None
        """
        ## insert the data into original_data table
        result = r.db('Traffic').table('original_data').insert(data).run()
        original_data_id = result['generated_keys'][0]

        created_timestamp = parser.parse(data['CREATED_TIMESTAMP'])
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
                            'created_timestamp': r.expr(created_timestamp).run()
                        }
                        SHP_list = copy.deepcopy(FI_item['SHP'])
                        FI_item['SHP'] = "See table road_data"
                        result = r.db('Traffic').table('flow_data').insert(FI_item).run()
                        flow_data_id = result['generated_keys'][0]
                        
                        for SHP_item in SHP_list:
                            SHP_item['flow_data_id'] = flow_data_id
                            try:
                                SHP_item['geometry'] = r.line(r.args(self.parse_SHP_values(SHP_item['value']))).run()
                                SHP_item['created_timestamp'] = r.expr(created_timestamp).run()
                                r.db('Traffic').table('road_data').insert(SHP_item).run()
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
        r.db('Traffic').table_create('original_data').run()
        r.db('Traffic').table_create('road_data').run()
        r.db('Traffic').table_create('flow_data').run()
        # r.db('Traffic').table_create('meta_data').run() might not need it
        r.db('Traffic').table('road_data').index_create('geometry', geo=True).run()
        r.db('Traffic').table('road_data').index_create('created_timestamp').run()
        r.db('Traffic').table('flow_data').index_create('created_timestamp', r.row["CUSTOM"]["created_timestamp"]).run()


    def main_matrix_data(matrix: pd.DataFrame):
        pass


    def fetch_geojson_item(self, id: str) -> Dict:
        """
        inputs: id: str(a primary key of road_data table)

        This function uses a id(primary key) to fethe a geojson object from 
        the road_data database.

        Example output:
        {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [125.6, 10.1]
          },
          "properties": {
            "name": "Dinagat Islands"
          }
        }

        For more infomation about geojson, check out
        http://geojson.org/
        """
        data = r.db('Traffic').table('road_data').get(id).run()
        flow_data_id = data['flow_data_id']
        flow_data = r.db('Traffic').table('flow_data').get(flow_data_id).run()
        print(flow_data)
        geojson_properties = {'TMC': flow_data['TMC'], 'CF': flow_data['CF'][0]}
        geojson_geometry = r.db('Traffic').table('road_data').get(id)['geometry'].to_geojson().run()
        geojson_type = "Feature"

        return {"type": geojson_type, "geometry": geojson_geometry, "properties": geojson_properties}


