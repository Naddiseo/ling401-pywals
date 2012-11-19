from wals import WALS

class Feature(object):
	
	def __init__(self, name):
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
	
