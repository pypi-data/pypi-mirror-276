

#/
#
#
from .group import clique as clique_group
#
#
import somatic
#
import pathlib
from os.path import dirname, join, normpath
#
#\

def clique ():
	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("example")
	def example_command ():	
		print ("example")

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

	group.add_command (example_command)
	group.add_command (tutorial_command)

	
	group.add_command (clique_group ())

	
	group ()




#
