from genealogy import Genealogy  # , Family, Genus, Language
from feature import Feature
from area import get_area
with Genealogy() as g:
	
	for language_data in Feature('102A'):
		language = g.find_language_by_code(language_data['wals code'])
		
		language.area = get_area((language.lat, language.lng))
		
		if language.area == 'UNKNOWN': 
			print u"language {}({}, {}) is in {}".format(language.name, language.lat, language.lng, language.area)
		
		# print language
