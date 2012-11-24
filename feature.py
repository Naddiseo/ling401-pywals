from wals import WALS
from genealogy import Genealogy

class Feature(object):
	
	def __init__(self, name):
		g = Genealogy()
		
		data = WALS.get_feature(name)
		self.name = name
		self.description = WALS.FEATURE_MAP[name]
		self.feature_values = WALS.FEATURE_VALUES[name]
		self.data = {}
		
		for lang_code, value in data.items():
			language = g.find_language_by_code(lang_code)
			language.features[name] = self.feature_values[value]
			
			self.data[lang_code] = language
	
	def __len__(self):
		return len(self.data)
	
	def __getitem__(self, key):
		return self.data[key]
	
	def __setitem__(self, key, value):
		self.data[key] = value
	
	def __iter__(self):
		return iter(self.data.values())
	
	def keys(self):
		return iter(self.data.keys())
	
	def items(self):
		return iter(self.data.items())
	
	def values(self):
		return iter(self.data.values())
	
	def languages(self):
		return self.values()
