




'''
	from poetry_uv.adventures.ventures import retrieve_ventures
	the_ventures = retrieve_ventures ()
'''

#/
#
from .monetary.venture import monetary_venture
from .sanique.venture import sanique_venture
from .demux_hap.venture import demux_hap_venture
from .vv_turbo.venture_build import bun_venture_build	
from .vv_turbo.venture_dev import bun_venture_dev	
#
#
from poetry_uv._essence import retrieve_essence
#
#
from ventures import ventures_map
#
#\

def retrieve_ventures ():
	essence = retrieve_essence ()

	return ventures_map ({
		"map": essence ["ventures"] ["path"],
		"ventures": [
			demux_hap_venture (),
			bun_venture_build (),
		
			monetary_venture (),
			sanique_venture ()
		]
	})