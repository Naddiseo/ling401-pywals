import csv
import os
import re
import urllib3
from pprint import pformat

from bs4 import BeautifulSoup
from pygeocoder import Geocoder
import pygeocoder

http = urllib3.PoolManager(num_pools = 100)

def valid_node(n):
	s = unicode(n)
	return all([n, n is not None, len(s.strip())])

class WALS(object):
	GENEALOGY_PAGE = "http://wals.info/languoid/genealogy"
	FEATURE_PAGE = 'http://wals.info/feature/{}.tab?v2=cd00&v1=cfff&v3=c00d&v4=c909&v5=cff0'
	LANG_KML = 'http://wals.info/languoid/lect/wals_code_{}?tg_format=kml'
	get_code_rx = re.compile('^http://wals\.info/languoid/lect/wals_code_(\w+)$', re.U)
	
	GMAPS_FILE = 'gmaps_latlng.txt'
	GMAPS = {}
	
	@classmethod
	def load_countries(cls):
		if os.path.exists(cls.GMAPS_FILE):
			with open(cls.GMAPS_FILE) as fp:
				cls.GMAPS = eval(fp.read())
	
	@classmethod
	def save_countries(cls):
		with open(cls.GMAPS_FILE, 'w') as fp:
			fp.write(pformat(cls.GMAPS))
	
	@classmethod
	def get_page(cls, url, get = True, **kwargs):
		user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4"
		headers = {
			'User-Agent' : user_agent
		}
		
		if get:
			response = http.request('GET', url, kwargs, headers)
		
		return response
		
	@classmethod
	def save_page(cls, output, url, *args, **kwargs):
		response = cls.get_page(url, *args, **kwargs)
		
		fp = open(output, 'w')
		fp.write(response.data)
		fp.close()
	
	@classmethod
	def get_latlng(cls, code):
		print('Getting latlan for {}'.format(code))
		response = cls.get_page(cls.LANG_KML.format(code))
		dom = BeautifulSoup(response.data, 'xml')
		
		coords = dom.kml.Document.Placemark.Point.coordinates.text.split(',')
		return coords
	
	@classmethod
	def get_country(cls, lat, lng):
		if (lat, lng) not in cls.GMAPS:
			print('Getting country for {} {}'.format(lat, lng))
			try:
				g = Geocoder.reverse_geocode(float(lat), float(lng))
				cls.GMAPS[(lat, lng)] = g[0].country
			except pygeocoder.GeocoderError:
				return 'UNKNOWN'
		return cls.GMAPS[(lat, lng)]
	
	@classmethod
	def get_genealogy(cls, infile = 'genealogy.html', refresh = False):
		'''
		data[family][genus][language]
		'''
		if not (refresh and os.path.exists(infile)):
			cls.save_page(infile, cls.GENEALOGY_PAGE)
		
		cls.load_countries()
		
		data = {}
		
		try:
			dom = BeautifulSoup(open(infile).read())
			
			families = dom.find('div', {'id' : 'genealogy'}).ol
			
			for family in families.children:
				if not valid_node(family):
					continue
				family_link = family.find('a', {'class' : 'Family'})
				
				family_tree = {
					'__name__' : family_link.text,
					'__link__' : family_link.attrs['href'],
				}
				
				for genus in family.ol.children:
					if not valid_node(genus):
						continue
					genus_link = genus.find('a', {'class' : 'Genus'})
					
					genus_tree = {
						'__name__' : genus_link.text,
						'__link__' : genus_link.attrs['href'],
						
					}
					
					for language in genus.ol.children:
						if not valid_node(language):
							continue
						language_link = language.find('a', {'class' : 'Language'})
						
						match = WALS.get_code_rx.search(language_link.attrs['href'])
						
						if match is None:
							print language_link.attrs['href']
							raise Exception(u'Bad href for {}'.format(language_link.text))
						
						code = match.group(1)
						lat, lng = cls.get_latlng(code)
						country = cls.get_country(lat, lng)
						genus_tree[language_link.text] = {
							'__name__' : language_link.text,
							'__link__' : language_link.attrs['href'],
							'__code__' : code,
							'__lat__' : lat,
							'__lng__' : lng,
							'__country__' : country,
						}
					
					family_tree[genus_link.text] = genus_tree
				
				data[family_link.text] = family_tree
		
		finally:
			cls.save_countries()
		
		return data
	
	@classmethod
	def get_feature(cls, feature, refresh = False):
		outfile = 'feature{}.tsv'.format(feature)
		if not (os.path.exists(outfile) or refresh):
			cls.save_page(outfile, cls.FEATURE_PAGE.format(feature))
		
		data = {}
		
		with open(outfile) as fp:
			fieldnames = []
			while True:
				line = fp.readline().strip()
				if line.split('\t')[0] == 'wals code':
					fieldnames = line.split('\t')
					break
			
			
			
			csvreader = csv.DictReader(fp, fieldnames = fieldnames, delimiter = '\t', quotechar = '"')
			for row in csvreader:
				data[row['wals code']] = row
		
		return data
