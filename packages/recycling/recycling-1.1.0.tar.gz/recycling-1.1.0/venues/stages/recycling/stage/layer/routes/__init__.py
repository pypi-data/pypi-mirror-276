


'''

'''

import recycling.stage.layer.routes.home.get as get_home_route
import recycling.stage.layer.routes.moves as moves_route
import recycling.stage.layer.routes.vue as vue_route

import recycling.stage.climate as stage_climate

def connect_routes (
	app,
	vue_dist_inventory
):
	climate = stage_climate.retrieve ()

	'''
		Vue
	'''
	vue_route.route (app, vue_dist_inventory)
	
	'''
		moves
	'''
	moves_route.route (app)

	@app.route ("/", methods = [ 'GET' ])
	def route_GET ():
		return get_home_route.present ()	

	@app.route ("/example", methods = [ 'GET' ])
	def route_GET_example ():
		return get_home_route.present ()

	return;