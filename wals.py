import csv
import os
import re
import urllib3

from bs4 import BeautifulSoup

import area

http = urllib3.PoolManager(num_pools = 100)

def valid_node(n):
	s = unicode(n)
	return all([n, n is not None, len(s.strip())])

class WALS(object):
	GENEALOGY_PAGE = "http://wals.info/languoid/genealogy"
	FEATURE_PAGE = 'http://wals.info/feature/{}.tab?v2=cd00&v1=cfff&v3=c00d&v4=c909&v5=cff0'
	LANG_KML = 'http://wals.info/languoid/lect/wals_code_{}?tg_format=kml'
	# LAT_LNG = 'http://www.findlatitudeandlongitude.com/processors/get-reverse-geocode.php?lat_in={}&lon_in={}&time={}'
	get_code_rx = re.compile('^http://wals\.info/languoid/lect/wals_code_(\w+)$', re.U)
	
	@classmethod
	def get_page(cls, url, get = True, **kwargs):
		user_agent = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13"
		
		headers = {
			'User-Agent' : user_agent
		}
		
		if get:
			attempts = 0
			while attempts < 10:
				try:
					response = http.request('GET', url, kwargs, headers)
				except:
					if attempts >= 10:
						raise
				attempts += 1
		
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
		try:
			coords = dom.kml.Document.Placemark.Point.coordinates.text.split(',')
		except AttributeError as e:
			print dom
			raise e
		return coords
	
	
	@classmethod
	def get_genealogy(cls, infile = 'genealogy.html', refresh = False):
		'''
		data[family][genus][language]
		'''
		if not (refresh and os.path.exists(infile)):
			cls.save_page(infile, cls.GENEALOGY_PAGE)
		
		
		data = {}
		
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
					#lng, lat = cls.get_latlng(code)
					genus_tree[language_link.text] = {
						'__name__' : language_link.text,
						'__link__' : language_link.attrs['href'],
						'__code__' : code,
						'__lat__' : '0',  #lat,
						'__lng__' : '0',  #,lng,
						'__area__' : 'UNKNOWN',
					}
				
				family_tree[genus_link.text] = genus_tree
			
			data[family_link.text] = family_tree
		
		return data
	
	@classmethod
	def get_feature(cls, feature, refresh = False):
		outfile = 'feature_data/feature{}.tsv'.format(feature)
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
