



import recycling.instrument.layer.start_dev as flask_start_dev

import os
from os.path import dirname, join, normpath
import pathlib
import sys
		
import asyncio
from websockets.sync.client import connect

async def async_search (port):
	address = f"ws://localhost:{ port }"
	
	with connect (address) as websocket:
		websocket.send ("Hello world!")
		message = websocket.recv ()
		
		print (f"Received: {message}")

	
		
def add ():
	import click
	@click.group ("sockets")
	def group ():
		pass


	'''
		./recycling instrument sockets --port 65000
	'''
	import click
	@group.command ("sockets")
	@click.option ('--port', '-np', default = '65000')
	def search (port):	
		CWD = os.getcwd ();
		
		import recycling.instrument.climate as instrument_climate
		instrument_climate.build (
			CWD
		)
	
		instrument_sockets.open (
			port = port
		)
	
		return;

	'''
		recycling_local sockets make_pouch --label instrument-1
	'''
	import click
	@group.command ("make_instrument")
	@click.option ('--label', required = True)
	@click.option ('--port', '-np', default = '65000')
	def search (label, port):	
		
		asyncio.run (async_search (port))	
		
	return group




#



