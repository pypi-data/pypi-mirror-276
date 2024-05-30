

#/
#
import recycling.instrument.clique as instrument_clique
import recycling.stage.clique as stage_clique
#
#
import somatic
#
#
import click
#
#
import pathlib
from os.path import dirname, join, normpath
#
#\

def intro ():
	@click.group ()
	def group ():
		pass

	@click.command ("tutorial")
	def tutorial_command ():	
		
		this_directory = str (pathlib.Path (__file__).parent.resolve ())
		module_directory = str (normpath (join (this_directory, "..")));
		
		somatic.start ({			
			#
			#	This is the node from which the traversal occur.
			#
			"directory": module_directory,
			
			#
			#	This path is removed from the absolute path of share files found.
			#
			"relative path": module_directory
		})
		
		import time
		while True:
			time.sleep (1000)

	group.add_command (tutorial_command)
	group.add_command (instrument_clique.start ())
	group.add_command (stage_clique.start ())
	
	return group;




#
