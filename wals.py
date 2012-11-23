import csv
import os

import area
from singleton import Singleton


class WALS(object):
	__metaclass__ = Singleton
	
	DATAPOINTS = 'wals_data/datapoints.csv'
	FEATURES = 'wals_data/features.csv'
	LANGUAGES = 'wals_data/languages.csv'
	VALUES = 'wals_data/languages.csv'
	
	
	@classmethod
	def get_genealogy(cls, infile = 'genealogy.html', refresh = False):
		'''
		data[family][genus][language]
		'''
		data = {}
		
		with open(cls.LANGUAGES) as fp:
			fieldnames = fp.readline().strip().split(',')
			csvreader = csv.DictReader(fp, fieldnames = fieldnames, delimiter = ',')
			for row in csvreader:
				
				data.setdefault(row['family'], {
					'__name__' : row['family']
				})
				data[row['family']].setdefault(row['genus'], {
					'__name__' : row['genus']
				})
				data[row['family']][row['genus']][row['name']] = {
					'__name__' : row['name'],
					'__code__' : row['wals code'],
					'__lat__' : row['latitude'],
					'__lng__' : row['longitude'],
					'__area__' : area.get_area((row['longitude'], row['latitude']))
				} 
		
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
