from genealogy import Genealogy  # , Family, Genus, Language
from feature import Feature
from area import NorthAmerica
with Genealogy() as g:
	
	for language_data in Feature('102A'):
		language = g.find_language_by_code(language_data['wals code'])
		
		if (language.lat, language.lng) in NorthAmerica:
			language.country = 'NORTH_AMERICA'
			print "language {}({}, {}) is in North America".format(language.name, language.lat, language.lng)
		
		print language
