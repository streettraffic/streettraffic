import rethinkdb as r
import json

print('loading data')
with open('C:/Users/shuang/App/RethinkDB/large.geojson', encoding="utf8") as data_file:
    data = json.load(data_file)

print('get geojson object')
for item in data['features']:
    item['geometry'] = r.geojson(item['geometry'])

print('dumping data into rethinkDB')
r.connect('localhost', 28015).repl()
#r.table_create('geo').run(conn)
r.table('geo').insert(data['features']).run()
