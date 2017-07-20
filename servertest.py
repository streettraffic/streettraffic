## import system module
import json
import rethinkdb as r
import time
import datetime as dt
import asyncio
import pstats, cProfile

## import custom module
from main_program.map_resource.utility import Utility
from main_program.database import TrafficData
from main_program import tools
from main_program.server import TrafficServer

class TestTrafficServer(TrafficServer):

    async def main_crawler(self):
        """
        """
        self.crawler_running = True
        while self.crawler_running:
            print('start crawling')
            self.traffic_data.store_matrix_json(self.traffic_matrix_list)
            #self.traffic_data.insert_analytics_traffic_pattern('[33.880079, 33.648894, -84.485086, -84.311365]')

            # time management, we want to execute script every 30 minutes
            # in order to do that we need to calculate how many seconds we should sleep
            current = dt.datetime.utcnow()
            if current.minute < 30:
                wait_seconds = 30*60 - current.minute*60 - current.second
            else:
                wait_seconds = 60*60 - current.minute*60 - current.second

            print('crawling finished')

            await asyncio.sleep(wait_seconds)    


settings = {
    'app_id': 'F8aPRXcW3MmyUvQ8Z3J9',
    'app_code' : 'IVp1_zoGHdLdz0GvD_Eqsw',
    'map_tile_base_url': 'https://1.traffic.maps.cit.api.here.com/maptile/2.1/traffictile/newest/normal.day/',
    'json_tile_base_url': 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?'
}

## initialize traffic server
traffic_server = TestTrafficServer(database_name= "Traffic", database_ip = "localhost")

# start
traffic_server.start()

#message = ['getMultipleDaysRouteTraffic', {'geocoded_waypoints': [{'geocoder_status': 'OK', 'place_id': 'ChIJleVd24sD9YgRk9wo-miJbik', 'types': ['street_address']}, {'geocoder_status': 'OK', 'place_id': 'Ei8yMCBQb25jZSBEZSBMZW9uIEF2ZSBORSwgQXRsYW50YSwgR0EgMzAzMDgsIFVTQQ', 'types': ['street_address']}], 'routes': [{'bounds': {'south': 33.754290000000005, 'west': -84.38942, 'north': 33.772310000000004, 'east': -84.37790000000001}, 'copyrights': 'Map data ©2017 Google', 'legs': [{'distance': {'text': '1.8 mi', 'value': 2921}, 'duration': {'text': '7 mins', 'value': 407}, 'end_address': '20 Ponce De Leon Ave NE, Atlanta, GA 30308, USA', 'end_location': {'lat': 33.7722607, 'lng': -84.38570179999999}, 'start_address': '209 Edgewood Ave NE, Atlanta, GA 30303, USA', 'start_location': {'lat': 33.7543628, 'lng': -84.37998879999998}, 'steps': [{'distance': {'text': '0.1 mi', 'value': 179}, 'duration': {'text': '1 min', 'value': 31}, 'end_location': {'lat': 33.7542857, 'lng': -84.37805500000002}, 'polyline': {'points': 'ws_mE|m_bO?cA@m@Fu@?_@@gA@sA?_@'}, 'start_location': {'lat': 33.7543628, 'lng': -84.37998879999998}, 'travel_mode': 'DRIVING', 'encoded_lat_lngs': 'ws_mE|m_bO?cA@m@Fu@?_@@gA@sA?_@', 'path': [{'lat': 33.754360000000005, 'lng': -84.37999}, {'lat': 33.754360000000005, 'lng': -84.37965000000001}, {'lat': 33.75435, 'lng': -84.37942000000001}, {'lat': 33.754310000000004, 'lng': -84.37915000000001}, {'lat': 33.754310000000004, 'lng': -84.37899}, {'lat': 33.7543, 'lng': -84.37863}, {'lat': 33.754290000000005, 'lng': -84.37821000000001}, {'lat': 33.754290000000005, 'lng': -84.37805}], 'lat_lngs': [{'lat': 33.754360000000005, 'lng': -84.37999}, {'lat': 33.754360000000005, 'lng': -84.37965000000001}, {'lat': 33.75435, 'lng': -84.37942000000001}, {'lat': 33.754310000000004, 'lng': -84.37915000000001}, {'lat': 33.754310000000004, 'lng': -84.37899}, {'lat': 33.7543, 'lng': -84.37863}, {'lat': 33.754290000000005, 'lng': -84.37821000000001}, {'lat': 33.754290000000005, 'lng': -84.37805}], 'instructions': 'Head <b>east</b> on <b>Edgewood Ave SE</b> toward <b>Bell St NE</b>', 'maneuver': '', 'start_point': {'lat': 33.7543628, 'lng': -84.37998879999998}, 'end_point': {'lat': 33.7542857, 'lng': -84.37805500000002}}, {'distance': {'text': '0.2 mi', 'value': 384}, 'duration': {'text': '2 mins', 'value': 90}, 'end_location': {'lat': 33.7577324, 'lng': -84.37790949999999}, 'maneuver': 'turn-left', 'polyline': {'points': 'is_mExa_bOYE{AEgACu@AI?sACyE?G?{BE'}, 'start_location': {'lat': 33.7542857, 'lng': -84.37805500000002}, 'travel_mode': 'DRIVING', 'encoded_lat_lngs': 'is_mExa_bOYE{AEgACu@AI?sACyE?G?{BE', 'path': [{'lat': 33.754290000000005, 'lng': -84.37805}, {'lat': 33.75442, 'lng': -84.37802}, {'lat': 33.75488, 'lng': -84.37799000000001}, {'lat': 33.75524, 'lng': -84.37797}, {'lat': 33.75551, 'lng': -84.37796}, {'lat': 33.75556, 'lng': -84.37796}, {'lat': 33.75598, 'lng': -84.37794000000001}, {'lat': 33.757070000000006, 'lng': -84.37794000000001}, {'lat': 33.757110000000004, 'lng': -84.37794000000001}, {'lat': 33.75773, 'lng': -84.37791}], 'lat_lngs': [{'lat': 33.754290000000005, 'lng': -84.37805}, {'lat': 33.75442, 'lng': -84.37802}, {'lat': 33.75488, 'lng': -84.37799000000001}, {'lat': 33.75524, 'lng': -84.37797}, {'lat': 33.75551, 'lng': -84.37796}, {'lat': 33.75556, 'lng': -84.37796}, {'lat': 33.75598, 'lng': -84.37794000000001}, {'lat': 33.757070000000006, 'lng': -84.37794000000001}, {'lat': 33.757110000000004, 'lng': -84.37794000000001}, {'lat': 33.75773, 'lng': -84.37791}], 'instructions': 'Turn <b>left</b> onto <b>Fort St NE</b>', 'start_point': {'lat': 33.7542857, 'lng': -84.37805500000002}, 'end_point': {'lat': 33.7577324, 'lng': -84.37790949999999}}, {'distance': {'text': '0.9 mi', 'value': 1489}, 'duration': {'text': '1 min', 'value': 82}, 'end_location': {'lat': 33.7673689, 'lng': -84.3885947}, 'polyline': {'points': 'yh`mE|`_bOa@AE?G@KBYF]TA@w@h@o@^o@RGBGDEDGJIRs@Tu@\\e@V[TA?i@^YRa@^QPSR_@b@WZm@|@sAnB{@hAABEFA??@A?GLA?ABkA~Am@z@mAvAy@bAq@t@{@x@y@v@C@URCBYX_@^{@bAQTSXc@n@Yf@CDGLUb@Qf@sBxEs@zACF_AhBADQXU`@]f@'}, 'start_location': {'lat': 33.7577324, 'lng': -84.37790949999999}, 'travel_mode': 'DRIVING', 'encoded_lat_lngs': 'yh`mE|`_bOa@AE?G@KBYF]TA@w@h@o@^o@RGBGDEDGJIRs@Tu@\\e@V[TA?i@^YRa@^QPSR_@b@WZm@|@sAnB{@hAABEFA??@A?GLA?ABkA~Am@z@mAvAy@bAq@t@{@x@y@v@C@URCBYX_@^{@bAQTSXc@n@Yf@CDGLUb@Qf@sBxEs@zACF_AhBADQXU`@]f@', 'path': [{'lat': 33.75773, 'lng': -84.37791}, {'lat': 33.7579, 'lng': -84.37790000000001}, {'lat': 33.75793, 'lng': -84.37790000000001}, {'lat': 33.75797, 'lng': -84.37791}, {'lat': 33.758030000000005, 'lng': -84.37793}, {'lat': 33.758160000000004, 'lng': -84.37797}, {'lat': 33.75831, 'lng': -84.37808000000001}, {'lat': 33.758320000000005, 'lng': -84.37809}, {'lat': 33.7586, 'lng': -84.37830000000001}, {'lat': 33.75884, 'lng': -84.37846}, {'lat': 33.759080000000004, 'lng': -84.37856000000001}, {'lat': 33.75912, 'lng': -84.37858000000001}, {'lat': 33.75916, 'lng': -84.37861000000001}, {'lat': 33.759190000000004, 'lng': -84.37864}, {'lat': 33.75923, 'lng': -84.37870000000001}, {'lat': 33.759280000000004, 'lng': -84.37880000000001}, {'lat': 33.75954, 'lng': -84.37891}, {'lat': 33.75981, 'lng': -84.37906000000001}, {'lat': 33.760000000000005, 'lng': -84.37918}, {'lat': 33.76014, 'lng': -84.37929000000001}, {'lat': 33.76015, 'lng': -84.37929000000001}, {'lat': 33.760360000000006, 'lng': -84.37945}, {'lat': 33.760490000000004, 'lng': -84.37955000000001}, {'lat': 33.76066, 'lng': -84.37971}, {'lat': 33.76075, 'lng': -84.3798}, {'lat': 33.760850000000005, 'lng': -84.3799}, {'lat': 33.761010000000006, 'lng': -84.38008}, {'lat': 33.76113, 'lng': -84.38022000000001}, {'lat': 33.76136, 'lng': -84.38053000000001}, {'lat': 33.76178, 'lng': -84.38109}, {'lat': 33.762080000000005, 'lng': -84.38146}, {'lat': 33.76209, 'lng': -84.38148000000001}, {'lat': 33.76212, 'lng': -84.38152000000001}, {'lat': 33.762130000000006, 'lng': -84.38152000000001}, {'lat': 33.762130000000006, 'lng': -84.38153000000001}, {'lat': 33.76214, 'lng': -84.38153000000001}, {'lat': 33.76218, 'lng': -84.3816}, {'lat': 33.762190000000004, 'lng': -84.3816}, {'lat': 33.7622, 'lng': -84.38162000000001}, {'lat': 33.76258, 'lng': -84.38210000000001}, {'lat': 33.76281, 'lng': -84.3824}, {'lat': 33.763200000000005, 'lng': -84.38284}, {'lat': 33.763490000000004, 'lng': -84.38318000000001}, {'lat': 33.763740000000006, 'lng': -84.38345000000001}, {'lat': 33.76404, 'lng': -84.38374}, {'lat': 33.76433, 'lng': -84.38402}, {'lat': 33.76435, 'lng': -84.38403000000001}, {'lat': 33.76446, 'lng': -84.38413000000001}, {'lat': 33.764480000000006, 'lng': -84.38415}, {'lat': 33.764610000000005, 'lng': -84.38428}, {'lat': 33.764770000000006, 'lng': -84.38444000000001}, {'lat': 33.76507, 'lng': -84.38478}, {'lat': 33.76516, 'lng': -84.38489000000001}, {'lat': 33.765260000000005, 'lng': -84.38502000000001}, {'lat': 33.765440000000005, 'lng': -84.38526}, {'lat': 33.765570000000004, 'lng': -84.38546000000001}, {'lat': 33.76559, 'lng': -84.38549}, {'lat': 33.76563, 'lng': -84.38556000000001}, {'lat': 33.76574, 'lng': -84.38574000000001}, {'lat': 33.76583, 'lng': -84.38594}, {'lat': 33.76641, 'lng': -84.38703000000001}, {'lat': 33.766670000000005, 'lng': -84.38749000000001}, {'lat': 33.766690000000004, 'lng': -84.38753000000001}, {'lat': 33.767010000000006, 'lng': -84.38806000000001}, {'lat': 33.76702, 'lng': -84.38809}, {'lat': 33.76711, 'lng': -84.38822}, {'lat': 33.76722, 'lng': -84.38839}, {'lat': 33.76737, 'lng': -84.38859000000001}], 'lat_lngs': [{'lat': 33.75773, 'lng': -84.37791}, {'lat': 33.7579, 'lng': -84.37790000000001}, {'lat': 33.75793, 'lng': -84.37790000000001}, {'lat': 33.75797, 'lng': -84.37791}, {'lat': 33.758030000000005, 'lng': -84.37793}, {'lat': 33.758160000000004, 'lng': -84.37797}, {'lat': 33.75831, 'lng': -84.37808000000001}, {'lat': 33.758320000000005, 'lng': -84.37809}, {'lat': 33.7586, 'lng': -84.37830000000001}, {'lat': 33.75884, 'lng': -84.37846}, {'lat': 33.759080000000004, 'lng': -84.37856000000001}, {'lat': 33.75912, 'lng': -84.37858000000001}, {'lat': 33.75916, 'lng': -84.37861000000001}, {'lat': 33.759190000000004, 'lng': -84.37864}, {'lat': 33.75923, 'lng': -84.37870000000001}, {'lat': 33.759280000000004, 'lng': -84.37880000000001}, {'lat': 33.75954, 'lng': -84.37891}, {'lat': 33.75981, 'lng': -84.37906000000001}, {'lat': 33.760000000000005, 'lng': -84.37918}, {'lat': 33.76014, 'lng': -84.37929000000001}, {'lat': 33.76015, 'lng': -84.37929000000001}, {'lat': 33.760360000000006, 'lng': -84.37945}, {'lat': 33.760490000000004, 'lng': -84.37955000000001}, {'lat': 33.76066, 'lng': -84.37971}, {'lat': 33.76075, 'lng': -84.3798}, {'lat': 33.760850000000005, 'lng': -84.3799}, {'lat': 33.761010000000006, 'lng': -84.38008}, {'lat': 33.76113, 'lng': -84.38022000000001}, {'lat': 33.76136, 'lng': -84.38053000000001}, {'lat': 33.76178, 'lng': -84.38109}, {'lat': 33.762080000000005, 'lng': -84.38146}, {'lat': 33.76209, 'lng': -84.38148000000001}, {'lat': 33.76212, 'lng': -84.38152000000001}, {'lat': 33.762130000000006, 'lng': -84.38152000000001}, {'lat': 33.762130000000006, 'lng': -84.38153000000001}, {'lat': 33.76214, 'lng': -84.38153000000001}, {'lat': 33.76218, 'lng': -84.3816}, {'lat': 33.762190000000004, 'lng': -84.3816}, {'lat': 33.7622, 'lng': -84.38162000000001}, {'lat': 33.76258, 'lng': -84.38210000000001}, {'lat': 33.76281, 'lng': -84.3824}, {'lat': 33.763200000000005, 'lng': -84.38284}, {'lat': 33.763490000000004, 'lng': -84.38318000000001}, {'lat': 33.763740000000006, 'lng': -84.38345000000001}, {'lat': 33.76404, 'lng': -84.38374}, {'lat': 33.76433, 'lng': -84.38402}, {'lat': 33.76435, 'lng': -84.38403000000001}, {'lat': 33.76446, 'lng': -84.38413000000001}, {'lat': 33.764480000000006, 'lng': -84.38415}, {'lat': 33.764610000000005, 'lng': -84.38428}, {'lat': 33.764770000000006, 'lng': -84.38444000000001}, {'lat': 33.76507, 'lng': -84.38478}, {'lat': 33.76516, 'lng': -84.38489000000001}, {'lat': 33.765260000000005, 'lng': -84.38502000000001}, {'lat': 33.765440000000005, 'lng': -84.38526}, {'lat': 33.765570000000004, 'lng': -84.38546000000001}, {'lat': 33.76559, 'lng': -84.38549}, {'lat': 33.76563, 'lng': -84.38556000000001}, {'lat': 33.76574, 'lng': -84.38574000000001}, {'lat': 33.76583, 'lng': -84.38594}, {'lat': 33.76641, 'lng': -84.38703000000001}, {'lat': 33.766670000000005, 'lng': -84.38749000000001}, {'lat': 33.766690000000004, 'lng': -84.38753000000001}, {'lat': 33.767010000000006, 'lng': -84.38806000000001}, {'lat': 33.76702, 'lng': -84.38809}, {'lat': 33.76711, 'lng': -84.38822}, {'lat': 33.76722, 'lng': -84.38839}, {'lat': 33.76737, 'lng': -84.38859000000001}], 'instructions': 'Take the ramp onto <b>I-75 N</b>/<b>I-85 N</b>', 'maneuver': '', 'start_point': {'lat': 33.7577324, 'lng': -84.37790949999999}, 'end_point': {'lat': 33.7673689, 'lng': -84.3885947}}, {'distance': {'text': '0.2 mi', 'value': 295}, 'duration': {'text': '1 min', 'value': 43}, 'end_location': {'lat': 33.7695827, 'lng': -84.38889879999999}, 'maneuver': 'ramp-right', 'polyline': {'points': 'aebmEtcabOEACACAA?A?C?A?A??@A?A@A?c@d@m@b@WPWPQFKFKD[H[HSD_@FQ@I?I?G?GAEAC?GAECGCMICCCCCCACACCGCGAIAGAK?M'}, 'start_location': {'lat': 33.7673689, 'lng': -84.3885947}, 'travel_mode': 'DRIVING', 'encoded_lat_lngs': 'aebmEtcabOEACACAA?A?C?A?A??@A?A@A?c@d@m@b@WPWPQFKFKD[H[HSD_@FQ@I?I?G?GAEAC?GAECGCMICCCCCCACACCGCGAIAGAK?M', 'path': [{'lat': 33.76737, 'lng': -84.38859000000001}, {'lat': 33.7674, 'lng': -84.38858}, {'lat': 33.76742, 'lng': -84.38857}, {'lat': 33.76744, 'lng': -84.38856000000001}, {'lat': 33.767450000000004, 'lng': -84.38856000000001}, {'lat': 33.76746, 'lng': -84.38856000000001}, {'lat': 33.767480000000006, 'lng': -84.38856000000001}, {'lat': 33.76749, 'lng': -84.38856000000001}, {'lat': 33.767500000000005, 'lng': -84.38856000000001}, {'lat': 33.767500000000005, 'lng': -84.38857}, {'lat': 33.76751, 'lng': -84.38857}, {'lat': 33.767520000000005, 'lng': -84.38858}, {'lat': 33.76753, 'lng': -84.38858}, {'lat': 33.76771, 'lng': -84.38877000000001}, {'lat': 33.76794, 'lng': -84.38895000000001}, {'lat': 33.768060000000006, 'lng': -84.38904000000001}, {'lat': 33.76818, 'lng': -84.38913000000001}, {'lat': 33.76827, 'lng': -84.38917000000001}, {'lat': 33.768330000000006, 'lng': -84.38921}, {'lat': 33.768390000000004, 'lng': -84.38924}, {'lat': 33.768530000000005, 'lng': -84.38929}, {'lat': 33.76867, 'lng': -84.38934}, {'lat': 33.76877, 'lng': -84.38937000000001}, {'lat': 33.768930000000005, 'lng': -84.38941000000001}, {'lat': 33.769020000000005, 'lng': -84.38942}, {'lat': 33.76907, 'lng': -84.38942}, {'lat': 33.76912, 'lng': -84.38942}, {'lat': 33.76916, 'lng': -84.38942}, {'lat': 33.769200000000005, 'lng': -84.38941000000001}, {'lat': 33.76923, 'lng': -84.38940000000001}, {'lat': 33.76925, 'lng': -84.38940000000001}, {'lat': 33.769290000000005, 'lng': -84.38939}, {'lat': 33.76932, 'lng': -84.38937000000001}, {'lat': 33.769360000000006, 'lng': -84.38935000000001}, {'lat': 33.76943, 'lng': -84.3893}, {'lat': 33.769450000000006, 'lng': -84.38928000000001}, {'lat': 33.769470000000005, 'lng': -84.38926000000001}, {'lat': 33.769490000000005, 'lng': -84.38924}, {'lat': 33.7695, 'lng': -84.38922000000001}, {'lat': 33.769510000000004, 'lng': -84.3892}, {'lat': 33.76953, 'lng': -84.38916}, {'lat': 33.76955, 'lng': -84.38912}, {'lat': 33.769560000000006, 'lng': -84.38907}, {'lat': 33.76957, 'lng': -84.38903}, {'lat': 33.769580000000005, 'lng': -84.38897}, {'lat': 33.769580000000005, 'lng': -84.3889}], 'lat_lngs': [{'lat': 33.76737, 'lng': -84.38859000000001}, {'lat': 33.7674, 'lng': -84.38858}, {'lat': 33.76742, 'lng': -84.38857}, {'lat': 33.76744, 'lng': -84.38856000000001}, {'lat': 33.767450000000004, 'lng': -84.38856000000001}, {'lat': 33.76746, 'lng': -84.38856000000001}, {'lat': 33.767480000000006, 'lng': -84.38856000000001}, {'lat': 33.76749, 'lng': -84.38856000000001}, {'lat': 33.767500000000005, 'lng': -84.38856000000001}, {'lat': 33.767500000000005, 'lng': -84.38857}, {'lat': 33.76751, 'lng': -84.38857}, {'lat': 33.767520000000005, 'lng': -84.38858}, {'lat': 33.76753, 'lng': -84.38858}, {'lat': 33.76771, 'lng': -84.38877000000001}, {'lat': 33.76794, 'lng': -84.38895000000001}, {'lat': 33.768060000000006, 'lng': -84.38904000000001}, {'lat': 33.76818, 'lng': -84.38913000000001}, {'lat': 33.76827, 'lng': -84.38917000000001}, {'lat': 33.768330000000006, 'lng': -84.38921}, {'lat': 33.768390000000004, 'lng': -84.38924}, {'lat': 33.768530000000005, 'lng': -84.38929}, {'lat': 33.76867, 'lng': -84.38934}, {'lat': 33.76877, 'lng': -84.38937000000001}, {'lat': 33.768930000000005, 'lng': -84.38941000000001}, {'lat': 33.769020000000005, 'lng': -84.38942}, {'lat': 33.76907, 'lng': -84.38942}, {'lat': 33.76912, 'lng': -84.38942}, {'lat': 33.76916, 'lng': -84.38942}, {'lat': 33.769200000000005, 'lng': -84.38941000000001}, {'lat': 33.76923, 'lng': -84.38940000000001}, {'lat': 33.76925, 'lng': -84.38940000000001}, {'lat': 33.769290000000005, 'lng': -84.38939}, {'lat': 33.76932, 'lng': -84.38937000000001}, {'lat': 33.769360000000006, 'lng': -84.38935000000001}, {'lat': 33.76943, 'lng': -84.3893}, {'lat': 33.769450000000006, 'lng': -84.38928000000001}, {'lat': 33.769470000000005, 'lng': -84.38926000000001}, {'lat': 33.769490000000005, 'lng': -84.38924}, {'lat': 33.7695, 'lng': -84.38922000000001}, {'lat': 33.769510000000004, 'lng': -84.3892}, {'lat': 33.76953, 'lng': -84.38916}, {'lat': 33.76955, 'lng': -84.38912}, {'lat': 33.769560000000006, 'lng': -84.38907}, {'lat': 33.76957, 'lng': -84.38903}, {'lat': 33.769580000000005, 'lng': -84.38897}, {'lat': 33.769580000000005, 'lng': -84.3889}], 'instructions': 'Take exit <b>249D</b> toward <b>US-19</b>/<b>US 29 N</b>/<b>W Peachtree St</b>', 'start_point': {'lat': 33.7673689, 'lng': -84.3885947}, 'end_point': {'lat': 33.7695827, 'lng': -84.38889879999999}}, {'distance': {'text': '453 ft', 'value': 138}, 'duration': {'text': '1 min', 'value': 46}, 'end_location': {'lat': 33.7697749, 'lng': -84.38743799999997}, 'polyline': {'points': '{rbmEreabO?[AKCEACA]AIAIAG?GAEAOESAIAMCOAM?OAQ?m@'}, 'start_location': {'lat': 33.7695827, 'lng': -84.38889879999999}, 'travel_mode': 'DRIVING', 'encoded_lat_lngs': '{rbmEreabO?[AKCEACA]AIAIAG?GAEAOESAIAMCOAM?OAQ?m@', 'path': [{'lat': 33.769580000000005, 'lng': -84.3889}, {'lat': 33.769580000000005, 'lng': -84.38876}, {'lat': 33.76959, 'lng': -84.3887}, {'lat': 33.76961, 'lng': -84.38867}, {'lat': 33.76962, 'lng': -84.38865000000001}, {'lat': 33.76963, 'lng': -84.38850000000001}, {'lat': 33.76964, 'lng': -84.38845}, {'lat': 33.769650000000006, 'lng': -84.3884}, {'lat': 33.76966, 'lng': -84.38836}, {'lat': 33.76966, 'lng': -84.38832000000001}, {'lat': 33.769670000000005, 'lng': -84.38829000000001}, {'lat': 33.76968, 'lng': -84.38821}, {'lat': 33.76971, 'lng': -84.38811000000001}, {'lat': 33.76972, 'lng': -84.38806000000001}, {'lat': 33.76973, 'lng': -84.38799}, {'lat': 33.76975, 'lng': -84.38791}, {'lat': 33.769760000000005, 'lng': -84.38784000000001}, {'lat': 33.769760000000005, 'lng': -84.38776}, {'lat': 33.76977, 'lng': -84.38767}, {'lat': 33.76977, 'lng': -84.38744000000001}], 'lat_lngs': [{'lat': 33.769580000000005, 'lng': -84.3889}, {'lat': 33.769580000000005, 'lng': -84.38876}, {'lat': 33.76959, 'lng': -84.3887}, {'lat': 33.76961, 'lng': -84.38867}, {'lat': 33.76962, 'lng': -84.38865000000001}, {'lat': 33.76963, 'lng': -84.38850000000001}, {'lat': 33.76964, 'lng': -84.38845}, {'lat': 33.769650000000006, 'lng': -84.3884}, {'lat': 33.76966, 'lng': -84.38836}, {'lat': 33.76966, 'lng': -84.38832000000001}, {'lat': 33.769670000000005, 'lng': -84.38829000000001}, {'lat': 33.76968, 'lng': -84.38821}, {'lat': 33.76971, 'lng': -84.38811000000001}, {'lat': 33.76972, 'lng': -84.38806000000001}, {'lat': 33.76973, 'lng': -84.38799}, {'lat': 33.76975, 'lng': -84.38791}, {'lat': 33.769760000000005, 'lng': -84.38784000000001}, {'lat': 33.769760000000005, 'lng': -84.38776}, {'lat': 33.76977, 'lng': -84.38767}, {'lat': 33.76977, 'lng': -84.38744000000001}], 'instructions': 'Continue onto <b>Linden Ave NW</b>', 'maneuver': '', 'start_point': {'lat': 33.7695827, 'lng': -84.38889879999999}, 'end_point': {'lat': 33.7697749, 'lng': -84.38743799999997}}, {'distance': {'text': '0.2 mi', 'value': 282}, 'duration': {'text': '1 min', 'value': 69}, 'end_location': {'lat': 33.7723136, 'lng': -84.38736919999997}, 'maneuver': 'turn-left', 'polyline': {'points': 'atbmEn|`bOo@?{BAM?a@?mAAo@?_@Ai@AwAE'}, 'start_location': {'lat': 33.7697749, 'lng': -84.38743799999997}, 'travel_mode': 'DRIVING', 'encoded_lat_lngs': 'atbmEn|`bOo@?{BAM?a@?mAAo@?_@Ai@AwAE', 'path': [{'lat': 33.76977, 'lng': -84.38744000000001}, {'lat': 33.770010000000006, 'lng': -84.38744000000001}, {'lat': 33.770630000000004, 'lng': -84.38743000000001}, {'lat': 33.770700000000005, 'lng': -84.38743000000001}, {'lat': 33.77087, 'lng': -84.38743000000001}, {'lat': 33.771260000000005, 'lng': -84.38742}, {'lat': 33.7715, 'lng': -84.38742}, {'lat': 33.771660000000004, 'lng': -84.38741}, {'lat': 33.77187, 'lng': -84.38740000000001}, {'lat': 33.772310000000004, 'lng': -84.38737}], 'lat_lngs': [{'lat': 33.76977, 'lng': -84.38744000000001}, {'lat': 33.770010000000006, 'lng': -84.38744000000001}, {'lat': 33.770630000000004, 'lng': -84.38743000000001}, {'lat': 33.770700000000005, 'lng': -84.38743000000001}, {'lat': 33.77087, 'lng': -84.38743000000001}, {'lat': 33.771260000000005, 'lng': -84.38742}, {'lat': 33.7715, 'lng': -84.38742}, {'lat': 33.771660000000004, 'lng': -84.38741}, {'lat': 33.77187, 'lng': -84.38740000000001}, {'lat': 33.772310000000004, 'lng': -84.38737}], 'instructions': 'Turn <b>left</b> onto <b>West Peachtree St NW</b>', 'start_point': {'lat': 33.7697749, 'lng': -84.38743799999997}, 'end_point': {'lat': 33.7723136, 'lng': -84.38736919999997}}, {'distance': {'text': '0.1 mi', 'value': 154}, 'duration': {'text': '1 min', 'value': 46}, 'end_location': {'lat': 33.7722607, 'lng': -84.38570179999999}, 'maneuver': 'turn-right', 'polyline': {'points': '}ccmE`|`bOBi@@[?U?K@[?C?wA?M@aA?]'}, 'start_location': {'lat': 33.7723136, 'lng': -84.38736919999997}, 'travel_mode': 'DRIVING', 'encoded_lat_lngs': '}ccmE`|`bOBi@@[?U?K@[?C?wA?M@aA?]', 'path': [{'lat': 33.772310000000004, 'lng': -84.38737}, {'lat': 33.772290000000005, 'lng': -84.38716000000001}, {'lat': 33.77228, 'lng': -84.38702}, {'lat': 33.77228, 'lng': -84.38691}, {'lat': 33.77228, 'lng': -84.38685000000001}, {'lat': 33.772270000000006, 'lng': -84.38671000000001}, {'lat': 33.772270000000006, 'lng': -84.38669}, {'lat': 33.772270000000006, 'lng': -84.38625}, {'lat': 33.772270000000006, 'lng': -84.38618000000001}, {'lat': 33.77226, 'lng': -84.38585}, {'lat': 33.77226, 'lng': -84.3857}], 'lat_lngs': [{'lat': 33.772310000000004, 'lng': -84.38737}, {'lat': 33.772290000000005, 'lng': -84.38716000000001}, {'lat': 33.77228, 'lng': -84.38702}, {'lat': 33.77228, 'lng': -84.38691}, {'lat': 33.77228, 'lng': -84.38685000000001}, {'lat': 33.772270000000006, 'lng': -84.38671000000001}, {'lat': 33.772270000000006, 'lng': -84.38669}, {'lat': 33.772270000000006, 'lng': -84.38625}, {'lat': 33.772270000000006, 'lng': -84.38618000000001}, {'lat': 33.77226, 'lng': -84.38585}, {'lat': 33.77226, 'lng': -84.3857}], 'instructions': 'Turn <b>right</b> onto <b>Ponce De Leon Ave NE</b>', 'start_point': {'lat': 33.7723136, 'lng': -84.38736919999997}, 'end_point': {'lat': 33.7722607, 'lng': -84.38570179999999}}], 'traffic_speed_entry': [], 'via_waypoint': [], 'via_waypoints': []}], 'overview_polyline': 'ws_mE|m_bO@qBFuAB{C?_@YEcDI_AAmHCcCEg@ASDYF]Ty@j@o@^o@ROHMPIRs@T{At@]TcAr@s@p@s@v@eAxAqC|DaBzB{BrCkBxBuBpBw@r@{AbBe@n@aA|AcDrHyBrEg@z@]f@EAGCC?G@i@f@eAt@i@XWLw@Rs@L[@_@CYIYUKWEk@Ag@EIGy@Iq@Iu@Aa@?m@o@?iCAoBAoAAaCGDgB@eC@_B', 'summary': 'I-75 N/I-85 N', 'warnings': [], 'waypoint_order': [], 'overview_path': [{'lat': 33.754360000000005, 'lng': -84.37999}, {'lat': 33.75435, 'lng': -84.37942000000001}, {'lat': 33.754310000000004, 'lng': -84.37899}, {'lat': 33.754290000000005, 'lng': -84.37821000000001}, {'lat': 33.754290000000005, 'lng': -84.37805}, {'lat': 33.75442, 'lng': -84.37802}, {'lat': 33.75524, 'lng': -84.37797}, {'lat': 33.75556, 'lng': -84.37796}, {'lat': 33.757070000000006, 'lng': -84.37794000000001}, {'lat': 33.75773, 'lng': -84.37791}, {'lat': 33.75793, 'lng': -84.37790000000001}, {'lat': 33.758030000000005, 'lng': -84.37793}, {'lat': 33.758160000000004, 'lng': -84.37797}, {'lat': 33.75831, 'lng': -84.37808000000001}, {'lat': 33.7586, 'lng': -84.37830000000001}, {'lat': 33.75884, 'lng': -84.37846}, {'lat': 33.759080000000004, 'lng': -84.37856000000001}, {'lat': 33.75916, 'lng': -84.37861000000001}, {'lat': 33.75923, 'lng': -84.37870000000001}, {'lat': 33.759280000000004, 'lng': -84.37880000000001}, {'lat': 33.75954, 'lng': -84.37891}, {'lat': 33.760000000000005, 'lng': -84.37918}, {'lat': 33.76015, 'lng': -84.37929000000001}, {'lat': 33.760490000000004, 'lng': -84.37955000000001}, {'lat': 33.76075, 'lng': -84.3798}, {'lat': 33.761010000000006, 'lng': -84.38008}, {'lat': 33.76136, 'lng': -84.38053000000001}, {'lat': 33.76209, 'lng': -84.38148000000001}, {'lat': 33.76258, 'lng': -84.38210000000001}, {'lat': 33.763200000000005, 'lng': -84.38284}, {'lat': 33.763740000000006, 'lng': -84.38345000000001}, {'lat': 33.76433, 'lng': -84.38402}, {'lat': 33.764610000000005, 'lng': -84.38428}, {'lat': 33.76507, 'lng': -84.38478}, {'lat': 33.765260000000005, 'lng': -84.38502000000001}, {'lat': 33.76559, 'lng': -84.38549}, {'lat': 33.76641, 'lng': -84.38703000000001}, {'lat': 33.76702, 'lng': -84.38809}, {'lat': 33.76722, 'lng': -84.38839}, {'lat': 33.76737, 'lng': -84.38859000000001}, {'lat': 33.7674, 'lng': -84.38858}, {'lat': 33.76744, 'lng': -84.38856000000001}, {'lat': 33.76746, 'lng': -84.38856000000001}, {'lat': 33.767500000000005, 'lng': -84.38857}, {'lat': 33.76771, 'lng': -84.38877000000001}, {'lat': 33.768060000000006, 'lng': -84.38904000000001}, {'lat': 33.76827, 'lng': -84.38917000000001}, {'lat': 33.768390000000004, 'lng': -84.38924}, {'lat': 33.76867, 'lng': -84.38934}, {'lat': 33.768930000000005, 'lng': -84.38941000000001}, {'lat': 33.76907, 'lng': -84.38942}, {'lat': 33.76923, 'lng': -84.38940000000001}, {'lat': 33.769360000000006, 'lng': -84.38935000000001}, {'lat': 33.769490000000005, 'lng': -84.38924}, {'lat': 33.76955, 'lng': -84.38912}, {'lat': 33.769580000000005, 'lng': -84.3889}, {'lat': 33.76959, 'lng': -84.3887}, {'lat': 33.76962, 'lng': -84.38865000000001}, {'lat': 33.76966, 'lng': -84.38836}, {'lat': 33.76971, 'lng': -84.38811000000001}, {'lat': 33.769760000000005, 'lng': -84.38784000000001}, {'lat': 33.76977, 'lng': -84.38767}, {'lat': 33.76977, 'lng': -84.38744000000001}, {'lat': 33.770010000000006, 'lng': -84.38744000000001}, {'lat': 33.770700000000005, 'lng': -84.38743000000001}, {'lat': 33.771260000000005, 'lng': -84.38742}, {'lat': 33.771660000000004, 'lng': -84.38741}, {'lat': 33.772310000000004, 'lng': -84.38737}, {'lat': 33.77228, 'lng': -84.38685000000001}, {'lat': 33.772270000000006, 'lng': -84.38618000000001}, {'lat': 33.77226, 'lng': -84.3857}]}], 'status': 'OK', 'request': {'origin': {'lat': 33.7544084, 'lng': -84.3799879}, 'destination': {'lat': 33.7725845, 'lng': -84.38560280000002}, 'travelMode': 'DRIVING'}}, [['2017-07-02T18:00:00.000Z', '2017-07-03T00:00:00.000Z'], ['2017-07-03T18:00:00.000Z', '2017-07-04T00:00:00.000Z'], ['2017-07-04T18:00:00.000Z', '2017-07-05T00:00:00.000Z'], ['2017-07-05T18:00:00.000Z', '2017-07-06T00:00:00.000Z']]]


#traffic_server.traffic_data.get_historic_traffic_multiple_days(message[1], message[2])

# cProfile.run("traffic_server.traffic_data.get_historic_traffic_multiple_days(message[1], message[2])", "Profile.prof")
# s = pstats.Stats("Profile.prof")
# s.strip_dirs().sort_stats("time").print_stats()