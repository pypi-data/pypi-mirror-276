

'''
	mongod --dbpath ./../_mongo_data --port 39000
'''

'''
	from poetry_uv.monetary.node.on import turn_on_monetary_node
	mongo_process = turn_on_monetary_node (
		poetry_uv_essence = poetry_uv_essence,
		
		exception_if_on = True
	)
	
	import time
	while True:
		time.sleep (1)
'''

'''	
	mongo_process.terminate ()

	#
	#	without this it might appear as if the process is still running.
	#
	import time
	time.sleep (2)
'''




#/
#
from .status import check_monetary_status
#
from poetry_uv._essence import retrieve_essence
from poetry_uv.adventures.alerting.parse_exception import parse_exception
from poetry_uv.adventures.alerting import activate_alert	
#
#
from biotech.topics.show.variable import show_variable		
import ships.cycle.loops as cycle_loops	
from ventures.utilities.hike_passive_forks import hike_passive_forks
#
#
import rich
#
#
from fractions import Fraction
import multiprocessing
import subprocess
import time
import os
import atexit
#
#\


def turn_on_the_node ():
	essence = retrieve_essence ()

	if ("onsite" in essence ["monetary"]):
		port = essence ["monetary"] ["onsite"] ["port"]
		dbpath = essence ["monetary"] ["onsite"] ["path"]
		PID_path = essence ["monetary"] ["onsite"] ["PID_path"]
		logs_path = essence ["monetary"] ["onsite"] ["logs_path"]

		os.makedirs (dbpath, exist_ok = True)
		os.makedirs (os.path.dirname (logs_path), exist_ok = True)
		os.makedirs (os.path.dirname (PID_path), exist_ok = True)

		'''
		script = [
			"mongod", 

			'--fork',

			'--dbpath', 
			#f"'{ dbpath }'", 
			f"{ dbpath }", 
			
			'--logpath',
			f"{ logs_path }", 
		
			
			'--port', 
			str (port),
			
			'--bind_ip',
			'0.0.0.0',
			
			'--pidfilepath',
			str (PID_path)
		]
		'''
		
		'''
		activate_alert ("info", {
			"procedure": script
		})
		'''

		#mongo_process = procedure.implicit (script)
		env_vars = os.environ.copy ()

		hike_passive_forks ({
			"script": " ".join ([
				"mongod", 

				'--fork',

				'--dbpath', 
				#f"'{ dbpath }'", 
				f"{ dbpath }", 
				
				'--logpath',
				f"{ logs_path }", 
			
				
				'--port', 
				str (port),
				
				'--bind_ip',
				'0.0.0.0',
				
				'--pidfilepath',
				str (PID_path)
			]),
			"Popen": {
				#"cwd": harbor_path,
				"env": env_vars,
				"shell": True
			}
		})


def turn_on_monetary_node (
	exception_if_on = False
):
	essence = retrieve_essence ()

	show_variable ("checking if the monetary is already on")

	turn_on_the_node ()

		


	

	
	
	


#
#
#