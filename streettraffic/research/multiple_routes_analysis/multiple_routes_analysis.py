## import system module
import json
import rethinkdb as r
import time
import datetime as dt
import asyncio
from shapely.geometry import Point, Polygon
import random
import pandas as pd
import os

## import custom module
import main_program
from main_program.map_resource import ultil
from main_program.database import TrafficData
from main_program import tools
from main_program.server import TrafficServer


def get_random_point_in_polygon(poly):
     (minx, miny, maxx, maxy) = poly.bounds
     while True:
         p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
         if poly.contains(p):
             return p

atlanta_polygon = Polygon([[33.658529, -84.471782], [33.667928, -84.351730], [33.883809, -84.347570], [33.855681, -84.469405]])
sample_points = []
for i in range(100):
    point_in_poly = get_random_point_in_polygon(atlanta_polygon)
    sample_points += [[point_in_poly.x, point_in_poly.y]]

## Copy the following points and plot it in https://www.darrinward.com/lat-long/
# print(TrafficData.format_list_points_for_display(sample_points))

sample_route_count = 100
route_obj_collection = []
for i in range(sample_route_count):
    point_in_poly1 = get_random_point_in_polygon(atlanta_polygon)
    point_in_poly2 = get_random_point_in_polygon(atlanta_polygon)
    route_obj_collection += [[
    {
        "lat": point_in_poly1.x,
        "lng": point_in_poly1.y
    },
    {
        "lat": point_in_poly2.x,
        "lng": point_in_poly2.y
    }
    ]]
    
route_obj_collection_json = json.dumps(route_obj_collection)

## An Example of route_obj_collection_json looks like the following
# route_obj_collection_json = '[[{"lat": 33.799087515810896, "lng": -84.4174599752579}, {"lat": 33.74258541519564, "lng": -84.40049923479191}], [{"lat": 33.75667708316275, "lng": -84.36617105743875}, {"lat": 33.72272993907663, "lng": -84.43918930257797}], [{"lat": 33.747825325840914, "lng": -84.39982695458436}, {"lat": 33.69803953408487, "lng": -84.35297580263247}]]'
    
## Copy route_obj_collection_json to the /Main/RouteLab routes of the web UI and follow the steps
## The result from /Main/RouteLab should look like this
with open('route_traffic_pattern_collection.json') as f:
    route_traffic_pattern_collection = json.load(f)

## Only take the longgest 20 routes for analysis
def overview_path_distance(overview_path):
    """
    This function extracts the longest_n routes in route_traffic_pattern_collection
    """
    distance = 0
    for i in range(len(overview_path)-1):
        point1 = overview_path[i]
        point2 = overview_path[i+1]
        distance += ultil.get_distance([point1['lat'], point1['lng']], [point2['lat'], point2['lng']])
    return distance
    
            

## Analyzing data
df = pd.DataFrame(index = [json.dumps(item['origin_destination']) for item in route_traffic_pattern_collection])
df['distance (in meters)'] = [overview_path_distance(item['route']['routes'][0]['overview_path']) for item in route_traffic_pattern_collection]
for i in range(len(route_traffic_pattern_collection[0]['chartLabel'])):
    df[route_traffic_pattern_collection[0]['chartLabel'][i]] = [item['chartData'][i] for item in route_traffic_pattern_collection]

df.sort_values(by='distance (in meters)')
#
#print(df.mean(axis=1))
#print(df.std())
#print(df.median())


# ======================================================
#route_traffic_pattern_collection = json.loads('[{"route":[{"lat":33.799087515810896,"lng":-84.4174599752579},{"lat":33.74258541519564,"lng":-84.40049923479191}],"chartLabel":["12:00:00 AM","12:30:00 AM","1:00:00 AM","1:30:00 AM","2:00:00 AM","2:30:00 AM","3:00:00 AM","3:30:00 AM","4:00:00 AM","4:30:00 AM","5:00:00 AM","5:30:00 AM","6:00:00 AM","6:30:00 AM","7:00:00 AM","7:30:00 AM","8:00:00 AM","8:30:00 AM","9:00:00 AM","9:30:00 AM","10:00:00 AM","10:30:00 AM","11:00:00 AM","11:30:00 AM","12:00:00 PM","12:30:00 PM","1:00:00 PM","1:30:00 PM","2:00:00 PM","2:30:00 PM","3:00:00 PM","3:30:00 PM","4:00:00 PM","4:30:00 PM","5:00:00 PM","5:30:00 PM","6:00:00 PM","6:30:00 PM","7:00:00 PM","7:30:00 PM","8:00:00 PM","8:30:00 PM","9:00:00 PM","9:30:00 PM","10:00:00 PM","10:30:00 PM","11:00:00 PM","11:30:00 PM"],"chartData":[0.3348513670212766,0.09341834574468086,0.2862373510638298,0.11529704787234044,0.09971518085106384,0.15456584574468088,0.19040912234042545,0.09148231914893619,0.17227737765957438,0.09792223404255318,0.2259118882978724,0.23501162765957448,0.17965792553191492,0.27221515957446807,0.43133886702127655,0.7718017765957447,1.1333522872340427,1.4242623031914894,1.535503707446809,0.9453390957446808,0.9957148776595742,1.3963468191489359,1.7928078563829786,1.581501702127659,1.9402515265957454,2.200531324468086,2.2442146436170214,2.275829617021277,2.378171941489361,2.456211579787234,2.9228462606382966,3.2007971968085105,3.6359411542553177,3.515899287234041,3.7099623244680853,3.892301297872341,4.310471026595745,3.7551886489361683,2.84991660106383,2.2118128723404253,1.5786782074468086,1.4011316648936165,1.5634196010638295,1.8509561329787227,1.8518717021276594,1.4274920053191484,1.0013004946808508,0.7835195744680852]},{"route":[{"lat":33.75667708316275,"lng":-84.36617105743875},{"lat":33.72272993907663,"lng":-84.43918930257797}],"chartLabel":["12:00:00 AM","12:30:00 AM","1:00:00 AM","1:30:00 AM","2:00:00 AM","2:30:00 AM","3:00:00 AM","3:30:00 AM","4:00:00 AM","4:30:00 AM","5:00:00 AM","5:30:00 AM","6:00:00 AM","6:30:00 AM","7:00:00 AM","7:30:00 AM","8:00:00 AM","8:30:00 AM","9:00:00 AM","9:30:00 AM","10:00:00 AM","10:30:00 AM","11:00:00 AM","11:30:00 AM","12:00:00 PM","12:30:00 PM","1:00:00 PM","1:30:00 PM","2:00:00 PM","2:30:00 PM","3:00:00 PM","3:30:00 PM","4:00:00 PM","4:30:00 PM","5:00:00 PM","5:30:00 PM","6:00:00 PM","6:30:00 PM","7:00:00 PM","7:30:00 PM","8:00:00 PM","8:30:00 PM","9:00:00 PM","9:30:00 PM","10:00:00 PM","10:30:00 PM","11:00:00 PM","11:30:00 PM"],"chartData":[0.27577873880597015,0.09164794029850747,0.1810330746268657,0.04079438059701492,0.07605019402985073,0.08656383582089552,0.06969781343283582,0.08223792537313433,0.07265826119402985,0.08490197014925374,0.11508218656716418,0.12925725373134328,0.25248157462686566,0.2765511716417911,0.3173636194029851,0.5842050223880597,0.88362676119403,0.9879103731343284,1.0881058208955225,0.9250897089552239,1.2101476716417912,0.9976162164179108,1.1241286865671642,1.0042773059701493,1.6472343507462681,1.6857909179104476,1.1831446343283583,1.3326690597014923,1.3112476567164177,1.542693574626865,1.541748917910448,1.4828469776119402,2.21435556716418,1.9597464626865673,1.9101857761194032,2.409968723880597,2.1658362611940296,1.676170731343283,1.4982358582089546,1.328247119402985,1.5561747313432839,1.04789226119403,1.1156997462686566,1.3474938283582079,1.2103893880597016,1.3713493731343287,0.7704790597014926,0.33243707462686567]},{"route":[{"lat":33.747825325840914,"lng":-84.39982695458436},{"lat":33.69803953408487,"lng":-84.35297580263247}],"chartLabel":["12:00:00 AM","12:30:00 AM","1:00:00 AM","1:30:00 AM","2:00:00 AM","2:30:00 AM","3:00:00 AM","3:30:00 AM","4:00:00 AM","4:30:00 AM","5:00:00 AM","5:30:00 AM","6:00:00 AM","6:30:00 AM","7:00:00 AM","7:30:00 AM","8:00:00 AM","8:30:00 AM","9:00:00 AM","9:30:00 AM","10:00:00 AM","10:30:00 AM","11:00:00 AM","11:30:00 AM","12:00:00 PM","12:30:00 PM","1:00:00 PM","1:30:00 PM","2:00:00 PM","2:30:00 PM","3:00:00 PM","3:30:00 PM","4:00:00 PM","4:30:00 PM","5:00:00 PM","5:30:00 PM","6:00:00 PM","6:30:00 PM","7:00:00 PM","7:30:00 PM","8:00:00 PM","8:30:00 PM","9:00:00 PM","9:30:00 PM","10:00:00 PM","10:30:00 PM","11:00:00 PM","11:30:00 PM"],"chartData":[0.07978895131086142,0.07321528089887641,0.047579456928838956,0.11933317415730338,0.09931571161048688,0.10096414794007492,0.09053383895131087,0.03383832397003746,0.056643455056179765,0.07137549625468163,0.08852409176029963,0.16739019662921353,0.20554859550561802,0.27163155430711616,0.479961563670412,0.8824367509363296,1.1565891573033706,1.1192594475655429,1.2260668258426963,1.1004719756554304,1.056173492509363,1.1230702340823968,1.1189424438202242,1.1909790262172284,1.1518267602996253,1.2877499438202251,1.1699865355805246,1.068427968164794,1.1110314325842694,1.2403556367041197,1.2044159644194756,1.0802583988764045,1.2111914794007492,1.215833192883895,1.6640983520599248,1.981399466292135,1.9035764981273398,1.465332106741573,1.0154324063670415,1.1651033988764046,1.069390299625468,1.1786476404494381,0.9851172191011237,0.9815651685393256,0.9666619288389514,0.8236693352059921,0.6420858426966293,0.12816136704119852]}]')
#df = pd.DataFrame(index = [json.dumps(item['route']) for item in route_traffic_pattern_collection])
#for i in range(len(route_traffic_pattern_collection[0]['chartLabel'])):
#    df[route_traffic_pattern_collection[0]['chartLabel'][i]] = [item['chartData'][i] for item in route_traffic_pattern_collection]
#
#print(df.mean())
#print(df.std())
#print(df.median())
