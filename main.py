from collections import namedtuple, OrderedDict

from tableprint import pprinttable

from dryer import dryer_method, dryer_method2

def get_data_for_table(*features):
	
	if len(features) > 1:
		data = dryer_method2(*features)
	else:
		data = dryer_method(features[0])
	
	columns = sorted(str(k) for k in data.keys())
	Row = namedtuple('Row', ['Feature'] + columns)
	
	def data_to_rows(data):
		rows = OrderedDict()
		
		for area, features in data.items():
			for feature_name, genus_count in features.items():
				default_dict = { c : 0 for c in columns}
				default_dict.update(Feature = feature_name)
				rows.setdefault(feature_name, default_dict)
				
				rows[feature_name][area] = genus_count
		
		return list(Row(**d) for d in rows.values())
	
	return data_to_rows(data)

pprinttable(get_data_for_table('102A'))
pprinttable(get_data_for_table('23A'))
pprinttable(get_data_for_table('102A', '23A'))
#

	
