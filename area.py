
class Area(object):
	NORTH_AMERICA = [
		74.402, -169.101,
		4.2, -168.398,
		3.5, -81.914,
		14.944, -72.422,
		49.838, -44.649,
		64.321, -60.117,
		74.590, -64.687
	
	]
	SOUTH_AMERICA = []
	INDO_EUROPEAN = []
	EAST_ASIA = []
	AUSTRALIASTIA = []
	
	def __init__(self, data):
		self.data = ((x, y) for x, y in data)
	
	def __contains__(self, other):
		if not isinstance(other, (tuple, list)):
			return False
		
		if len(other) != 2:
			return False
		
		poly = self.data
		num = len(self.data)
		i = 0
		j = num - 1
		c = 0
		x, y = other
		
		for i in xrange(num):
			if  ((poly[i][1] > y) != (poly[j][1] > y)) and \
				(x < (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1]) + poly[i][0]):
				c = not c
			j = i
			
			
		return bool(c)


NorthAmerica = Area(Area.NORTH_AMERICA)
SouthAmerica = Area(Area.SOUTH_AMERICA)
IndoEurope = Area(Area.INDO_EUROPEAN)
Asia = Area(Area.EAST_ASIA)
Australia = Area(Area.AUSTRALIASTIA)

def get_area(coords):
	select = {
		NorthAmerica : 'NORTH_AMERICA',
		SouthAmerica : 'SOUTH_AMERICA',
		IndoEurope : 'EUROPE',
		Asia : 'EAST_ASIA',
		Australia : 'AUSTRALIAL_AND_NG'
	}
	
	for area, value in select.items():
		if coords in area:
			return value
	
	return 'UNKNOWN'
