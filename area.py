
class Poly(object):
	def __init__(self, data):
		self.data = tuple((x, y) for x, y in data)
	
	@property
	def x_coords(self):
		return list(y for _, y in self.data) + [self.data[0][1]]
	
	@property
	def y_coords(self):
		return list(x for x, _ in self.data) + [self.data[0][0]]
	
	def __len__(self):
		return len(self.data)
	
	def __getitem__(self, key):
		return self.data[key]
	
class Area(object):
	NORTH_AMERICA = [[
		(74.402, -169.101),
		(4.2, -168.398),
		(3.5, -81.914),
		(14.944, -72.422),
		(49.838, -44.649),
		(64.321, -60.117),
		(74.590, -64.687)
	
	]]
	SOUTH_AMERICA = [[
		(2.46, -82.969),
		(13.582, -75.586),
		(13.239, -65.390),
		(-2.46, -26.016),
		(-59.534, -48.867),
		(-60.240, -94.922),
	]]
	EUROPE_ASIA = [[
		(36.386, -5.977),
		(37.230, 0.264),
		(39.0277, 5.713),
		(38.891, 11.953),
		(37.649, 12.480),
		(35.604, 13.975),
		(34.452, 25.576),
		(33.943, 33.223),
		(27.684, 34.717),
		(16.383, 42.363),
		(12.811, 44.385),
		(13.838, 51.592),
		(14.094, 75.510),
		(4.040, 76.904),
		(3.513, 90.088),
		(-11.867, 108.720),
		# (-11.781, 125.068),
		# (-6.665, 126.826),
		(-0.703, 122.695),
		(6.839, 130.891),
		(28.768, 139.482),
		(49.497, 164.443),
		(61.856, 180.0),  # (61.856, -173.232),
		(81.518, 171.738),
		(82.214, 6.504),
		(82.309, -58.887),
		(71.017, -60.644),
		(59.623, -45.527),
		(39.909, -15.293),
	],
	
	]
	AFRICA = [[
		(31.80, 33.223),
		(26.745, 35.507),
		(14.775, 42.363),
		(11.695, 44.473),
		(13.753, 55.371),
		(-15.792, 55.547),
		(-19.643, 65.039),
		(-38.823, 42.714),
		(-38.135, 7.910),
		(7.188, -16.699),
		(15.284, -29.004),
		(40.979, -32.519),
		(41.112, -21.973),
		(34.597, -10.723),
		(36.173, -4.92),
		(36.173, -1.934),
		(37.579, 3.340),
		(37.996, 10.020),
		(36.457, 12.480),
		(33.431, 18.105),
		(33.578, 26.016),
	]]
	AUSTRALIASTIA = [[
		# (-10.920, 126.287),
		# (-5.441, 126.045),
		# (-1.758, 124.738),
		(18.075, 142.826),
		# (2.724, 160.225),
		(18.523, 180.0),  # (-11.523, -164.004),
		(-56.268, 180.0),  # (-56.268, -156.006),
		(-55.826, 93.779),
		(-24.127, 90.615),
		(-15.284, 108.574),
		(-12.812, 110.826),
	]]
	
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
