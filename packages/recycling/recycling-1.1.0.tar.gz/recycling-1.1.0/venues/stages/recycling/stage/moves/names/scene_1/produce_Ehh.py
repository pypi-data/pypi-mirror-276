



import pymongo

import recycling.stage.climate as instrument_climate
import recycling.stage.moon.connect as moon_connect

'''
	
'''
def perform (fields):
	moon_connection = moon_connect.start ()
	scene_1 = moon_connection ["scenes"] ["scene-1"]

	existing_document = scene_1.find_one ({
		"move": "scene 1: produce Ehh"
	})
	if existing_document:
		return {
			"status": "fail",
			"note": "That move has already happened."
		}

	move_number = str (scene_1.count_documents ({}) + 1)

	scene_1.insert_one ({
		"move": "scene 1: produce Ehh",
		"move #": move_number,
		
		"amount": "1e36",
		"flavor": "ECC_448_2:3043300506032B6571033A00E701F06C74F2990640FBBB062B7E1D0D33C2EA2724F9FDD908CACF0F200270907A8400BD26B287335570F34FCA7B0ECD07B0D9622D5CE82A80"
	})


	return {
		"status": "pass"
	}
	
	
	
	
#