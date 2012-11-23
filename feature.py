from wals import WALS
from genealogy import Genealogy

class Feature(object):
	
	def __init__(self, name):
		self.name = name
		self.data = WALS.get_feature(name) 
	
	def __len__(self):
		return len(self.data)
	
	def __getitem__(self, key):
		return self.data[key]
	
	def __setitem__(self, key, value):
		self.data[key] = value
	
	def __iter__(self):
		return iter(self.data.values())
	
	def keys(self):
		return self.data.keys()
	
	def items(self):
		return self.data.items()
	
	def values(self):
		return self.data.values()
	
	def languages(self):
		g = Genealogy()
		for data in self:
			language = g.find_language_by_code(data['wals code'])
			language.features[self.name] = data['description']
			yield language
