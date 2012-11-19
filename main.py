from genealogy import Genealogy  # , Family, Genus, Language
from feature import Feature

with Genealogy() as g:
	
	for language in Feature('102A'):
		print g.find_language_by_code(language['wals code'])
		break

