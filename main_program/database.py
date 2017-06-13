import rethinkdb as r
from typing import Dict

class TrafficData:

    def __init__(self):
        pass

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
        unique_id = result['generated_keys'][0]

        ## 

        for RWS_item in data['RWS']:
            for RW_item in RWS_item['RW']:
                # will use RW_item['DE']
                for FIS_item in RW_item['FIS']:
                    for FI_item in FIS_item['FI']:
                        # our CUSTOM attributes
                        FI_item['CUSTOM'] = {
                            'parent_DE': RW_item['DE'],
                            'original_data_id': unique_id
                        }
                        r.db('Traffic').table('road_data').insert(FI_item).run()






    def read_traffic_data(url: str) -> Dict:
        pass

    def connect(self):
        r.connect('localhost', 28015).repl()


