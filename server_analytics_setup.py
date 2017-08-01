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
# server.traffic_matrix_list = [San_Francisco_matrix]



server.start()
conn = server.traffic_data.conn

# City Polygon
San_Francisco_polygon = [[37.837174338616975,-122.48725891113281],[37.83364941345965,-122.48485565185547],[37.83093781796035,-122.4814224243164],[37.82415839321614,-122.48004913330078],[37.8203616433087,-122.47970581054688],[37.81059767530207,-122.47798919677734],[37.806122091729485,-122.47627258300781],[37.79215110146845,-122.48039245605469],[37.78726741375342,-122.48519897460938],[37.78618210598413,-122.49927520751953],[37.78645343442073,-122.50614166259766],[37.779127216982424,-122.51232147216797],[37.772614414082014,-122.51163482666016],[37.76121562849642,-122.51197814941406],[37.75171529845649,-122.51060485839844],[37.74329970164702,-122.50957489013672],[37.735969208590504,-122.50717163085938],[37.73081027834234,-122.50717163085938],[37.72293542866175,-122.50682830810547],[37.715331331027045,-122.50442504882812],[37.714244967649265,-122.49893188476562],[37.71940505182832,-122.50030517578125],[37.724564776604836,-122.5030517578125],[37.729724141962045,-122.50167846679688],[37.7324394530424,-122.49549865722656],[37.72918106779786,-122.49378204345703],[37.729724141962045,-122.48828887939453],[37.72782336496339,-122.4807357788086],[37.73271097867418,-122.37945556640625],[37.74520008134973,-122.37533569335938],[37.74655746554895,-122.39112854003906],[37.75008654795525,-122.3873519897461],[37.754972691904946,-122.38391876220703],[37.76148704857093,-122.38597869873047],[37.769629187677005,-122.3876953125],[37.78265474565738,-122.38872528076172],[37.78781006166096,-122.3880386352539],[37.79594930209237,-122.37911224365234],[37.804358908571395,-122.36984252929688],[37.812767557570204,-122.3605728149414],[37.817649559511125,-122.35130310058594],[37.82009043941308,-122.332763671875],[37.823344820392535,-122.30632781982422],[37.8271414168374,-122.30701446533203],[37.824700770115996,-122.31765747070312],[37.82253123860035,-122.33139038085938],[37.8203616433087,-122.34615325927734],[37.81792077237497,-122.35576629638672],[37.81168262440736,-122.3653793334961],[37.803002585189645,-122.37396240234375],[37.790523241426946,-122.3880386352539],[37.79594930209237,-122.39490509033203],[37.80273131752431,-122.39936828613281],[37.80815648152641,-122.40726470947266],[37.80734273233311,-122.42305755615234],[37.807071480609274,-122.43267059326172],[37.80571520704469,-122.44194030761719],[37.80463017025873,-122.45189666748047],[37.80463017025873,-122.464599609375],[37.807071480609274,-122.47421264648438],[37.815208598896255,-122.47695922851562],[37.82768377181359,-122.47798919677734],[37.835276322922695,-122.48004913330078],[37.837174338616975,-122.48725891113281]]
Boston_polygon = [[42.32453946380133,-71.13029479980469],[42.32758538845383,-71.0489273071289],[42.330631165629846,-71.03588104248047],[42.33316920061984,-71.02180480957031],[42.339513840022754,-71.02455139160156],[42.3397676122846,-71.04412078857422],[42.34611158596906,-71.02558135986328],[42.356514317057886,-71.02317810058594],[42.348648996207956,-71.00669860839844],[42.35829022102701,-71.00360870361328],[42.353469793490646,-70.99090576171875],[42.36057345238455,-70.98918914794922],[42.363110278811256,-71.00223541259766],[42.37883631647602,-70.99983215332031],[42.37756823359386,-71.00738525390625],[42.37224200585402,-71.01631164550781],[42.37680737157286,-71.02008819580078],[42.381879610913195,-71.015625],[42.38999434161929,-71.00704193115234],[42.40444610741266,-71.00395202636719],[42.40444610741266,-71.13029479980469],[42.32453946380133,-71.13029479980469]]
Pittsburgh_polygon = [[40.603526799885884,-80.09445190429688],[40.564937785967224,-80.13427734375],[40.50126945841646,-80.14801025390625],[40.42290582797254,-80.12054443359375],[40.3549167507906,-80.1287841796875],[40.330842639095756,-80.14389038085938],[40.31199603742692,-80.16311645507812],[40.319325896602095,-79.9310302734375],[40.365381076021734,-79.80056762695312],[40.57119697629581,-79.7991943359375],[40.603526799885884,-80.09445190429688]]
Greenville_polygon = [[34.96531080784271,-82.44483947753906],[34.946176590087454,-82.44140625],[34.92422301690582,-82.45994567871094],[34.89888467073924,-82.46818542480469],[34.871285134570016,-82.47367858886719],[34.837477162415986,-82.452392578125],[34.83015027082022,-82.54096984863281],[34.820004267650454,-82.53822326660156],[34.829022998858306,-82.45101928710938],[34.8047829195724,-82.44071960449219],[34.79068657192738,-82.44552612304688],[34.770383597610255,-82.47573852539062],[34.76192255039478,-82.47024536132812],[34.784483415461345,-82.44415283203125],[34.7483830709853,-82.31849670410156],[34.71847552413778,-82.25944519042969],[34.72073307506407,-82.24845886230469],[34.75740963726007,-82.28141784667969],[34.77263973038464,-82.26699829101562],[34.83184114982865,-82.28965759277344],[34.86058077988933,-82.24845886230469],[34.86790496256872,-82.25601196289062],[34.839167890957015,-82.30133056640625],[34.86903170200862,-82.34458923339844],[34.96531080784271,-82.44483947753906]]
Norfolk_polygon = [[37.00693943418586,-76.32339477539062],[36.98884240936997,-76.31034851074219],[36.982260605282676,-76.30348205566406],[36.96799807635307,-76.30210876464844],[36.95976847846004,-76.27738952636719],[36.953732874654285,-76.2725830078125],[36.94769679250732,-76.28700256347656],[36.95098926024786,-76.29661560058594],[36.95757376878687,-76.30348205566406],[36.95976847846004,-76.31584167480469],[36.9669008480318,-76.32820129394531],[36.90323455156814,-76.32888793945312],[36.91366629380721,-76.31721496582031],[36.90927415514871,-76.28631591796875],[36.89499795802219,-76.28974914550781],[36.901587303978474,-76.30348205566406],[36.90323455156814,-76.31515502929688],[36.874127942666334,-76.32888793945312],[36.8631414329529,-76.30828857421875],[36.849955535919875,-76.32682800292969],[36.856548768788954,-76.34056091308594],[36.82852360193767,-76.33094787597656],[36.820278951308744,-76.34536743164062],[36.81203341240741,-76.34124755859375],[36.83017242546416,-76.28974914550781],[36.79993834872292,-76.2835693359375],[36.80323719192363,-76.19155883789062],[36.84116367417466,-76.19499206542969],[36.82137828938333,-76.1407470703125],[36.82577548376294,-76.04873657226562],[36.84281222525469,-76.04736328125],[36.85160389745116,-76.14280700683594],[36.92739009701458,-76.16065979003906],[36.93726970584893,-76.22039794921875],[36.96799807635307,-76.27670288085938],[36.96854668458301,-76.29592895507812],[36.98390610968992,-76.29936218261719],[37.00693943418586,-76.32339477539062]]
polygon_collection = [
    ['San_Francisco_polygon', San_Francisco_polygon],
    ['Boston_polygon', Boston_polygon], 
    ['Pittsburgh_polygon', Pittsburgh_polygon], 
    ['Greenville_polygon', Greenville_polygon], 
    ['Norfolk_polygon', Norfolk_polygon]
]


# setup monitoring area
#for polygon_item in polygon_collection:
#    server.traffic_data.set_traffic_patter_monitoring_area(polygon_item[1], description=polygon_item[0], grid_point_distance=1000, testing=True, force=True)

date = ["2017-07-13T04:00:00.000Z","2017-07-14T03:00:00.000Z"]
polygon_name_collection = ['San_Francisco_polygon', 'Boston_polygon', 'Pittsburgh_polygon', 'Greenville_polygon', 'Norfolk_polygon']
for polygon_name in polygon_name_collection:
    analytics_monitored_area_id = r.table('analytics_monitored_area').get_all(polygon_name, index="description").get_field('analytics_monitored_area_id').run(conn).next()
    server.traffic_data.insert_analytics_traffic_pattern_between("2017-07-13T04:00:00.000Z", "2017-07-14T04:00:00.000Z", analytics_monitored_area_id)
    
