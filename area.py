
class Poly(object):
	def __init__(self, data):
		self.data = tuple((lng, lat) for lng, lat in data)
	
	def __len__(self):
		return len(self.data)
	
	def __getitem__(self, key):
		return self.data[key]
	
	def longitudes(self):
		" The X coords - How far east or west"
		for lng, lat in self.data + (self.data[0],):
			yield lng
	
	def latitudes(self):
		" The Y coords - How far north or south"
		for lng, lat in self.data + (self.data[0],):
			yield lat

class Area(object):
	# long/lat
	NORTH_AMERICA = [[
		(-169.101, 74.402),
		(-169.101, 45.0),
		(-172.0, 45.0),
		(-172.0, 35.402),
		(-168.398, 4.2),
		(-81.914, 3.5),
		(-72.422, 14.844),
		(-60.0, 14.0),
		(-44.649, 49.838),
		(-60.117, 64.321),
		(-64.687, 74.590)
	
	]]
	SOUTH_AMERICA = [[
		(-82.75, 2.46),
		(-73.086, 13.582),
		(-65.390, 13.239),
		(-26.016, -2.46),
		(-48.867, -59.534),
		(-94.922, -60.240),
	]]
	EUROPE_ASIA = [[
		(-5.977, 36.386),
		(0.264, 37.230),
		(5.713, 39.0277),
		(11.953, 38.891),
		(12.480, 37.649),
		(13.975, 35.604),
		(25.576, 34.452),
		(33.223, 33.943),
		(34.717, 27.684),
		(42.363, 16.383),
		(44.385, 12.811),
		(51.592, 13.838),
		(70.510, 14.094),
		(70.904, 3.040),
		(90.088, 3.513),
		(108.720, -11.867),
		(122.0, -0.703),
		(130.0, 6.839),
		(139.482, 28.768),
		(164.443, 49.497),
		(180.0, 61.856),  # (61.856, -173.232),
		(171.738, 81.518),
		(6.504, 82.214),
		(-58.887, 82.309),
		(-60.644, 71.017),
		(-45.527, 59.623),
		(-15.293, 39.909),
	],
	[
		(-180.0, 74.0),
		(-180.0, 63.0),
		(-170.0, 63.0),
		(-170.0, 74.0)
	]
	]
	AFRICA = [[
		(33.223, 31.80),
		(35.507, 26.745),
		(42.363, 14.775),
		(44.473, 11.695),
		(55.371, 13.753),
		#(55.547, -15.792),
		(65.039, -19.643),
		(42.714, -38.823),
		(7.910, -38.135),
		(-16.699, 7.188),
		(-29.004, 15.284),
		(-32.519, 40.979),
		(-21.973, 41.112),
		(-10.723, 34.597),
		(-4.92, 36.173),
		(-1.934, 36.173),
		(3.340, 37.579),
		(10.020, 37.996),
		(12.480, 36.457),
		(18.105, 33.431),
		(26.016, 33.578),
	]]
	AUSTRALIASTIA = [[
		(142.826, 18.075),
		(180.0, 18.523),
		(180.0, -56.268),
		(93.779, -55.826),
		(90.615, -24.127),
		(106.574, -15.284),
		(108.826, -12.812),
	],
	[
		(-180.0, -8.5),
		(-105.0, -8.5),
		(-105.0, -30.0),
		(-180.0, -30.0)
	]
	]
	
	def __init__(self, data):
		self.data = tuple(Poly(poly) for poly in data)
	
	def __contains__(self, other):
		if not isinstance(other, (tuple, list)):
			return False
		
		if len(other) != 2:
			return False
		
		for poly in self.data:
			if Area._poly_contains_point(other, poly):
				return True
		
		return False
	
	def __iter__(self):
		for poly in self.data:
			yield poly
	
	@staticmethod
	def _poly_contains_point(point, poly):
		num = len(poly)
		i = 0
		j = num - 1
		c = 0
		x, y = map(float, point)
		
		for i in xrange(num):
			if  ((poly[i][1] > y) != (poly[j][1] > y)) and \
				(x < (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1]) + poly[i][0]):
				c = not c
			j = i
			
			
		return bool(c)

NorthAmerica = Area(Area.NORTH_AMERICA)
SouthAmerica = Area(Area.SOUTH_AMERICA)
EuropeAsia = Area(Area.EUROPE_ASIA)
Africa = Area(Area.AFRICA)
Australia = Area(Area.AUSTRALIASTIA)

def get_area(coords):
	select = {
		NorthAmerica : 'NORTH_AMERICA',
		SouthAmerica : 'SOUTH_AMERICA',
		EuropeAsia : 'EUROPE_ASIA',
		Africa : 'AFRICA',
		Australia : 'AUSTRALIAL_AND_NG'
	}
	
	for area, value in select.items():
		if coords in area:
			return value
	
	return 'UNKNOWN'
