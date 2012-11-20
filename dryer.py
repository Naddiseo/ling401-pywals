from genealogy import Genealogy
from feature import Feature


def dryer_data(feature_name):
	# data[area][genus][feature_value] = language_count
	data = {}
	
	g = Genealogy()
	
	for language_data in Feature(feature_name):
		language = g.find_language_by_code(language_data['wals code']) 
		area = language.area.name
		genus = language.genus.name
		value = language_data['description']
		
		data.setdefault(area, {})
		data[area].setdefault(genus, {})
		data[area][genus].setdefault(value, 0)
		data[area][genus][value] += 1
	
	return data

def dryer_analise(data):
	# ret[area][feature_value] = genus_count
	ret = {}
	
	for area, genus_map in data.items():
		ret.setdefault(area, {})
		
		for feature_map in genus_map.values():
			top_count = -1
			current_feature = None
			for feature_value, language_count in feature_map.items():
				ret[area].setdefault(feature_value, 0)
				
				if language_count > top_count:
					current_feature = feature_value
			
			ret[area][current_feature] += 1
			
			
	
	return ret

def dryer_method(feature_name):
	return dryer_analise(dryer_data(feature_name))
