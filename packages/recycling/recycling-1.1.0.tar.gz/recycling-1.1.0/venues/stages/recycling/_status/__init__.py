

#----
#
import biotech
#
#
import rich
#
#
import json
import pathlib
from os.path import dirname, join, normpath
import sys
#
#----


def start ():
	


	this_folder = pathlib.Path (__file__).parent.resolve ()
	stages = str (normpath (join (this_folder, "../../../stages")))


	#status_assurances_path = str (normpath (join (this_folder, "insurance")))
	status_assurances_path = str (normpath (join (this_folder, "..")))

	
	if (len (sys.argv) >= 2):
		glob_string = status_assurances_path + '/' + sys.argv [1]
		db_directory = False
	else:
		glob_string = status_assurances_path + '/**/status_*.py'
		db_directory = normpath (join (this_folder, "DB"))

	print ("glob string:", glob_string)

	scan = biotech.start (
		glob_string = glob_string,
		simultaneous = True,
		module_paths = [
			stages
		],
		relative_path = status_assurances_path,
		
		db_directory = db_directory
	)
	
	rich.print_json (data = scan)