

'''
	itinerary:
		[ ] pass the current python path to this procedure
'''


'''
	https://sanic.dev/en/guide/running/manager.html#dynamic-applications
'''

'''
	worker manager:
		https://sanic.dev/en/guide/running/manager.html
'''

'''
	Asynchronous Server Gateway Interface, ASGI:
		https://sanic.dev/en/guide/running/running.html#asgi
		
		uvicorn harbor:create
'''

'''
	Robyn, rust
		https://robyn.tech/
'''

'''
	--factory
'''

#/
#
#
from .guest_sockets import sockets_guest
#
from .guest_regions_vue import vue_regions
#
from poetry_uv.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
#
from poetry_uv._essence import retrieve_essence, build_essence
from poetry_uv.adventures.alerting import activate_alert
from poetry_uv.adventures.alerting.parse_exception import parse_exception
#
#
from biotech.topics.show.variable import show_variable
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi, Extend
#from sanic_openapi import swagger_blueprint, openapi_metadata
#from sanic_openapi import swagger_blueprint, doc
import sanic.response as sanic_response
#
#
import json
import os
import traceback
#
#\_

'''
	https://sanic.dev/en/guide/running/running.html#using-a-factory
'''
def create ():
	inspector_port = os.environ.get ('inspector_port')
	env_vars = os.environ.copy ()
	
	essence = retrieve_essence ()
	
	
	'''
		#
		#	https://sanic.dev/en/guide/running/configuration.html#inspector
		#
		INSPECTOR_PORT
	'''
	
	app = Sanic (__name__)
	
	app.extend (config = {
		"oas_url_prefix": "/docs",
		"swagger_ui_configuration": {
			"docExpansion": "list" # "none"
		},
	})
	
	#app.blueprint (swagger_blueprint)
	app.config.INSPECTOR = True
	app.config.INSPECTOR_HOST = "0.0.0.0"
	app.config.INSPECTOR_PORT = int (inspector_port)
	

	if (essence ["mode"] == "nurture"):
		#
		#	https://sanic.dev/en/plugins/sanic-ext/http/cors.html#configuration
		#
		#
		@app.middleware ('response')
		async def before_route_middleware (request, response):
			URL = request.url
			response.headers['Access-Control-Allow-Origin'] = '*'
			response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
			response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
			response.headers['Access-Control-Allow-Credentials'] = 'true'
			
			print ('Middleware before every route "response":', URL)
			
			return;

	
	#
	#	opener
	#
	#
	#app.ext.openapi.add_security_scheme ("api_key", "apiKey")
	app.ext.openapi.add_security_scheme ("api_key", "http")
	

	vue_regions ({
		"app": app
	})
	
	
	

		
	return app

