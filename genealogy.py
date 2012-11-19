from wals import WALS
import pprint
import os
from pprint import pformat

class Language(object):
	__slots__ = ('name', 'link', 'code', 'features', 'lat', 'lng', 'area')
	
	def __init__(self, data):
		if isinstance(data, Language):
			self.name = data.name
			self.link = data.link
			self.code = data.code
			self.lat = data.lat
			self.lng = data.lng
			self.area = data.area
			self.features = data.features
		else:
			self.name = data.pop('__name__')
			self.link = data.pop('__link__')
			self.code = data.pop('__code__')
			self.lat = data.pop('__lat__', '')
			self.lng = data.pop('__lng__', '')
			self.area = data.pop('__area__', 'UNKNOWN')
			self.features = {}
	
	def __unicode__(self):
		return 'Language({})'.format(pformat(dict(
			__name__ = self.name,
			__link__ = self.link,
			__code__ = self.code,
			__lat__ = self.lat,
			__lng__ = self.lng,
			__area__ = self.area
		)))
	
	__str__ = __unicode__
	__repr__ = __unicode__

class Genus(object):
	__slots__ = ('name', 'link', 'languages')
	
	def __init__(self, data):
		if isinstance(data, Genus):
			self.name = data.name
			self.link = data.name
			self.languages = data.languages
		else:
			self.name = data.pop('__name__')
			self.link = data.pop('__link__')
			self.languages = {}
		
		for _language in data.values():
			if isinstance(_language, Language):
				language = _language
			else:
				language = Language(_language)
			self.languages[language.name] = language
	
	def __unicode__(self):
		ret = dict(
			__name__ = self.name,
			__link__ = self.link,
		)
		
		for name, lang in self.languages.items():
			ret[name] = lang
		
		return 'Genus({})'.format(pformat(ret))
	
	def __getitem__(self, key):
		return self.languages[key]
	
	def __iter__(self):
		return iter(self.languages.values())
	
	__str__ = __unicode__
	__repr__ = __unicode__

class Family(object):
	__slots__ = ('name', 'link', 'genera')
	def __init__(self, data):
		if isinstance(data, Family):
			self.name = data.name
			self.link = data.link
			self.genera = data.genera
		else:
			self.name = data.pop('__name__')
			self.link = data.pop('__link__')
			self.genera = {}
			
			for _genus in data.values():
				if isinstance(_genus, Genus):
					genus = _genus
				else:
					genus = Genus(_genus)
				self.genera[genus.name] = genus
	
	def __unicode__(self):
		ret = dict(
			__name__ = self.name,
			__link__ = self.link,
		)
		for name, genus in self.genera.items():
			ret[name] = genus
		
		return 'Family({})'.format(pformat(ret)) 
	
	def __getitem__(self, key):
		return self.genera[key]
	
	def __iter__(self):
		return iter(self.genera.values())
	
	__str__ = __unicode__
	__repr__ = __unicode__
	
class Genealogy(object):
	LANG_DB = 'langdb.txt'
	GEN_HTML = 'genealogy.html'
	
	def __init__(self):
		self.families = {}
		
		
		if not os.path.exists(Genealogy.LANG_DB) or os.path.getsize(Genealogy.LANG_DB) < 100:
			self.reload()
		else:
			self.load_data()
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.save_data()
	
	def __iter__(self):
		for family in self.families.values():
			yield family
			
	
	def _load_from_data(self, data):
		for _family in data.values():
			if isinstance(_family, Family):
				family = _family
			else: 
				family = Family(_family)
			self.families[family.name] = family
	
	def load_data(self):
		with open(Genealogy.LANG_DB, 'r') as fp:
			data = eval(fp.read())
			self._load_from_data(data)
			
	
	def save_data(self):
		fp = open(Genealogy.LANG_DB, 'w')
		fp.write(pprint.pformat(self.families, width = 120))
		fp.close()
	
	def reload(self):
		data = WALS.get_genealogy(Genealogy.GEN_HTML, True)
		self._load_from_data(data)
			
		
	def find_language_by_code(self, code):
		for family in self:
			for genera in family:
				for language in genera:
					if language.code == code:
						return language
		raise Exception('Language code {} not found'.format(code))
	
