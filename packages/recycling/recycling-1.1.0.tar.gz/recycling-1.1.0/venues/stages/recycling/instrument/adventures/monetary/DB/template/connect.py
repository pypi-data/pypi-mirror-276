


'''	
	from poetry_uv.adventures.monetary.DB.poetry_uv_inventory.connect import connect_to_poetry_uv_inventory
	[ driver, poetry_uv_inventory_DB ] = connect_to_poetry_uv_inventory ()
	driver.close ()
'''

'''
	from poetry_uv.adventures.monetary.DB.poetry_uv_inventory.connect import connect_to_poetry_uv_inventory
	[ driver, poetry_uv_inventory_DB ] = connect_to_poetry_uv_inventory ()
	foods_collection = poetry_uv_inventory_DB ["foods"]	
	foods_collection.close ()
'''




from poetry_uv.adventures.monetary.moves.URL.retrieve import retreive_monetary_URL
from poetry_uv._essence import retrieve_essence
	
import pymongo

def connect_to_poetry_uv_inventory ():
	essence = retrieve_essence ()
	
	ingredients_DB_name = essence ["monetary"] ["databases"] ["template"] ["alias"]
	monetary_URL = retreive_monetary_URL ()

	driver = pymongo.MongoClient (monetary_URL)

	return [
		driver,
		driver [ ingredients_DB_name ]
	]