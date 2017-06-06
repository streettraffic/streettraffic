from ..HERE_map import ultil

def test_get_tile():
	"""
	The official example provided by HERE
	https://developer.here.com/rest-apis/documentation/enterprise-map-tile/topics/key-concepts.html
	"""
	assert ultil.get_tile(52.525439, 13.38727, 12) == (2200.317383111111, 1343.2026309543003)

def test_get_quadkeys():
	"""
	The official example provided by HERE
	https://developer.here.com/rest-apis/documentation/traffic/common/map_tile/topics/quadkeys.html
	"""
	assert ultil.get_quadkeys(35210, 21493, 16) == "1202102332221212"
