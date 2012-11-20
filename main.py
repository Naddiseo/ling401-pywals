from collections import namedtuple, OrderedDict

from dryer import dryer_method

from tableprint import pprinttable

data = dryer_method('102A')

columns = sorted(data.keys())

Row = namedtuple('Row', ('',) + columns)

def data_to_rows(data):
	rows = OrderedDict([
		(feature_name, Row()) for feature_name in data.values().keys()
	])
	
	for area, features in data.items():
		for feature_name, genus_count in features.items():
			setattr(rows[feature_name], area, genus_count)
	
	return rows.values()

pprinttable(data_to_rows(data))
