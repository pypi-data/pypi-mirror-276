







import pymongo

import recycling.instrument.climate as instrument_climate
import recycling.instrument.moon.connect as moon_connect

def perform (fields):
	moon_connection = moon_connect.start ()
	hotties = moon_connection ["pocket"] ["hotties"]
	
	documents_list = list (hotties.find ({}, { "_id": 0 }))
	print (documents_list)

	return {
		"status": "pass"
	}
	
	
	
	
#
