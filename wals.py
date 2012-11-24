import csv
import os

import area
from singleton import Singleton
from pprint import pprint


class WALS(object):
	__metaclass__ = Singleton
	
	DATAPOINTS = 'wals_data/datapoints.csv'
	FEATURES = 'wals_data/features.csv'
	LANGUAGES = 'wals_data/languages.csv'
	VALUES = 'wals_data/values.csv'
	
	FEATURE_MAP = {}
	FEATURE_VALUES = {}
	FEATURE_LANGUAGES = {}
	
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
	def get_feature(cls, feature):
		
		if not len(cls.FEATURE_MAP):
			with open(cls.FEATURES) as fp:
				fieldnames = fp.readline().strip().split(',')
				csvreader = csv.DictReader(fp, fieldnames = fieldnames)
				for row in csvreader:
					cls.FEATURE_MAP[row['id']] = row['name']
		
		if not len(cls.FEATURE_VALUES):
			with open(cls.VALUES) as fp:
				fieldnames = fp.readline().strip().split(',')
				csvreader = csv.DictReader(fp, fieldnames = fieldnames)
				for row in csvreader:
					feature_name = row['feature_id']
					value = row['value_id']
					description = row['description']
					long_desc = row['long description']
					
					cls.FEATURE_VALUES.setdefault(feature_name, {})
					cls.FEATURE_VALUES[feature_name][value] = dict(description = description, long_desc = long_desc, value = value)
		
		if not len(cls.FEATURE_LANGUAGES):
			with open(cls.DATAPOINTS) as fp:
				fieldnames = fp.readline().strip().split(',')
				csvreader = csv.DictReader(fp, fieldnames = fieldnames)
				for row in csvreader:
					
					for fieldname in fieldnames:
						if fieldname == 'wals_code':
							continue
						
						cls.FEATURE_LANGUAGES.setdefault(fieldname, {})
						if row[fieldname].strip() != '':
							cls.FEATURE_LANGUAGES[fieldname][row['wals_code']] = row[fieldname]
		
		return cls.FEATURE_LANGUAGES[feature]
