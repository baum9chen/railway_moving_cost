#coding: utf-8

import requests
import time

key = ''
with open("../data/key/key") as f:
          key = f.read()
        
url = 'https://api.ekispert.jp/v1/json/station'
params = {
	'key': key,
	'type': 'train',
	'offset': 1,
	'limit': 100,
	'gcs': 'wgs84'
}
max_cnt = -1
#max_cnt = 121
alldata = []

while True:
	print(f"requesting: offset={params['offset']} / {max_cnt}")
	response = requests.get(url, params=params)
	ret = response.json()

	if max_cnt < 0:
		max_cnt = int(ret['ResultSet']['max'])
		print(f'max_cnt: {max_cnt}')

	for p in ret['ResultSet']['Point']:
		# すべてstringで返ってくるっぽい
		data = [
			p['Station']['code'],
			p['Station']['Name'],
			p['Station']['Type'],
			p['Prefecture']['code'],
			p['Prefecture']['Name'],
			p['GeoPoint']['lati_d'],
			p['GeoPoint']['longi_d']
		]
		alldata.append('\t'.join(data))

	if params['offset'] + params['limit'] - 1 > max_cnt:
		break

	params['offset'] = params['offset'] + params['limit']
	time.sleep(1)

with open('../data/master/station_master.tsv', 'w') as f:
	f.write('\n'.join(alldata))

