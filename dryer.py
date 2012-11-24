from genealogy import Genealogy
from feature import Feature


def dryer_data(feature_name):
	# data[area][genus][feature_value] = language_count
	data = {}
	
	for language in Feature(feature_name):
		area = language.area
		genus = language.genus.name
		value = language.features[feature_name]['description']
		
		data.setdefault(area, {})
		data[area].setdefault(genus, {})
		data[area][genus].setdefault(value, 0)
		data[area][genus][value] += 1
	
	return data

def dryer_data2(*feature_names):
	# data[area][genus][(feature_values)] = langauge_count
	data = {}
	# Languages that all features have
	languages = set()
	
	g = Genealogy()
	feature = Feature(feature_names[0])
	
	for language in feature.languages():
		languages.add(language.code)
	
	for feature_name in feature_names:
		feature = Feature(feature_name)
		this_set = set()
		for language in feature.languages():
			this_set.add(language.code)
		
		languages &= this_set
	
	for language_code in languages:
		language = g.find_language_by_code(language_code)
		area = language.area
		genus = language.genus.name
		value = ','.join(v['description'] for v in sorted(language.features.values()))
		
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
					top_count = language_count
			
			ret[area][current_feature] += 1
	
	return ret

def dryer_method2(*feature_names):
	return dryer_analise(dryer_data2(*feature_names))

def dryer_method(feature_name):
	return dryer_analise(dryer_data(feature_name))
