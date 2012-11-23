import matplotlib.pyplot as plt
from area import Africa, Australia, EuropeAsia, NorthAmerica, SouthAmerica, \
	get_area
from genealogy import Genealogy
from feature import Feature
import math
IMAGE_CENTER = (773, 540)
IMAGE_PATH = 'worldimage.png'
IMAGE_DIMENSIONS = (1712, 897)

TOP = 85.675
RIGHT = 180 + (180 - 29.88)
BOTTOM = -76.542
LEFT = -180 - (180 - 87.187)

# TOP-BOTTOM
HEIGHT = 302.217
# RIGHT-LEFT 
WIDTH = 602.933


X_SCALE = lambda x: ((IMAGE_DIMENSIONS[0] * float(x)) / WIDTH) + IMAGE_CENTER[0]
Y_SCALE = lambda y: ((IMAGE_DIMENSIONS[1] * float(y)) / -HEIGHT) + IMAGE_CENTER[1]

def gd(x):
	return(2 * math.atan(math.e ** x)) - (math.pi / 2)

def Y_SCALE(y):
	try:
		ret = gd(y) * -IMAGE_DIMENSIONS[1] / HEIGHT
		print "ret={}".format(ret)
		#ret *= IMAGE_DIMENSIONS[1] / -HEIGHT
		ret += IMAGE_CENTER[1]
		#print "returning {} for {}".format(ret, y)
		return ret
	except ValueError:
		print "Error for {}".format(y)
		raise


def annotate(label, lng, lat):
	plt.annotate(
		label,
		xy = (X_SCALE(lng), Y_SCALE(lat)), xytext = (-10, 10),
		textcoords = 'offset points', ha = 'right', va = 'bottom',
		bbox = dict(boxstyle = 'round,pad=0.2', fc = 'yellow', alpha = 0.5),
		arrowprops = dict(arrowstyle = '->')
	)


def main():
	img = plt.imread(IMAGE_PATH)
	fig = plt.figure()
	plt.imshow(img,)
	
	for cont in [Australia, EuropeAsia, Africa, NorthAmerica, SouthAmerica]:
		
		for poly in cont:
			subplot = fig.add_subplot(111)
			subplot.plot(map(X_SCALE, poly.longitudes()), map(Y_SCALE, poly.latitudes()))
		
			#for x, y in poly.data[0:]:
			#	annotate(u"{},{}".format(x, y), x, y)

	#g = Genealogy() 
	
	for i in (0, -180, 180):
		for j in (0, 90, -90):
			annotate('{}, {}'.format(i, j), i, j)
	
	#i = 0
	#for language in g.languages():
	#	i += 1
	#	if i >= 30:
	#		break
	#	name = language.name.decode('utf-8')
	#	if language.area == 'UNKNOWN':
	#		#language.area = get_area((language.lat, language.lng))
	#		#print u"{}({}, {})".format(language.name, language.lat, language.lng)
	#		annotate(u"{}({:.3f}, {:.3f})".format(name, float(language.lat), float(language.lng)), language.lat, language.lng)
	#
	fig.show()

if __name__ == '__main__':
	main()
