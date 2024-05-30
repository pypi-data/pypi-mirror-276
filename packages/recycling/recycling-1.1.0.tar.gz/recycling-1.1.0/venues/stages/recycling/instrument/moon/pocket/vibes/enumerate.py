


'''
	import recycling.instrument.moon.pocket.vibes.enumerate as enumerate_vibes
	vibes = enumerate_vibes.start ()
'''

import pymongo

import recycling.instrument.moon.connect as moon_connect
import recycling.mixes.EEC_448_2.keys as EEC_448_2_key_creator	



def start ():
	moon_connection = moon_connect.start ()
	vibes = moon_connection ["pocket"] ["vibes"]
	
	all_documents = vibes.find ({}, { "_id": 0 })
	
	#print ("vibes:", all_documents)
	
	documents_list = [
		{ key: value for key, value in document.items () } for document in all_documents
	]
	
	return documents_list;