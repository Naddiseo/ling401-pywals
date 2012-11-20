import matplotlib.pyplot as plt
from area import Africa, Australia, EuropeAsia, NorthAmerica, SouthAmerica
from genealogy import Genealogy
from feature import Feature

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

img = plt.imread(IMAGE_PATH)

X_SCALE = lambda x: ((IMAGE_DIMENSIONS[0] * float(x)) / WIDTH) + IMAGE_CENTER[0]
Y_SCALE = lambda y: ((IMAGE_DIMENSIONS[1] * float(y)) / -HEIGHT) + IMAGE_CENTER[1]

fig = plt.figure()
plt.imshow(img,)

def annotate(label, lat, lng):
	plt.annotate(
		label,
		xy = (X_SCALE(lat), Y_SCALE(lng)), xytext = (-10, 10),
		textcoords = 'offset points', ha = 'right', va = 'bottom',
		bbox = dict(boxstyle = 'round,pad=0.2', fc = 'yellow', alpha = 0.5),
		arrowprops = dict(arrowstyle = '->')
	)

for cont in [Australia, EuropeAsia, Africa, NorthAmerica, SouthAmerica]:
	
	for poly in cont:
		subplot = fig.add_subplot(111)
		subplot.plot(map(X_SCALE, poly.x_coords), map(Y_SCALE, poly.y_coords))
	
		for y, x in poly.data[0:]:
			annotate("{},{}".format(y, x), x, y)

with Genealogy() as g:
	
	for language_data in Feature('102A'):
		language = g.find_language_by_code(language_data['wals code'])
		
		# language.area = get_area((language.lat, language.lng))
		
		if language.area == 'UNKNOWN': 
			print u"{}({}, {})".format(language.name, language.lat, language.lng)
			annotate(u"{}({:.3f}, {:.3f})".format(language.name, float(language.lat), float(language.lng)), language.lng, language.lat)

fig.show()
