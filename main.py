from collections import namedtuple, OrderedDict

from tableprint import pprinttable

from dryer import dryer_method
from genealogy import Genealogy
from area import get_area

data = dryer_method('23A')

columns = sorted(data.keys())
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

pprinttable(data_to_rows(data))


	
