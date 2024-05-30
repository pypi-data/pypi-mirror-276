


'''
	
'''

'''
	create_instrument
	
	fields {
		"CWD": CWD,
		"name": name,
		"layer port": layer_port,
		"mongo port": mongo_port
	}
'''





import os
from os.path import dirname, join, normpath
import pathlib
import sys
from multiprocessing import Process

from .start_mongo import perform as perform_start_mongo

import recycling.instrument.climate as instrument_climate
import recycling.instrument.layer.start_dev as flask_dev

import time

def perform (move):
	print ("start layer");

	assert ("CWD" in move)
	assert ("name" in move)
	assert ("layer port" in move)
	assert ("mongo port" in move)
	
	name = move ["name"]
	CWD = move ["CWD"]
	layer_port = move ["layer port"]
	mongo_port = move ["mongo port"]

	instrument_path = str (normpath (join (CWD, name)))
	instrument_climate.build (instrument_path = instrument_path)

	mongo_DB_directory = str (normpath (join (CWD, name, "mongo_DB_directory")))
	if (not os.path.exists (mongo_DB_directory)):			
		os.mkdir (mongo_DB_directory) 
		
	if (not os.path.isdir (mongo_DB_directory)):
		print ("There is already something at:", mongo_DB_directory)
		return;
	
	perform_start_mongo ({
		"CWD": CWD,
		"name": name,
		
		"mongo port": mongo_port,
		"mongo directory": mongo_DB_directory
	});
	
	time.sleep (2)

	flask_server = Process (
		target = flask_dev.start,
		args = (),
		kwargs = {
			"port": layer_port
		}
	)
	flask_server.start ()

	while True:
		time.sleep (1000)
