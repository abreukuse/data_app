"""
Query data from mongodb.
"""

import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
database = myclient['fee_database']

def find_document(query, city): 
	"""
	Find the document from the collections in mongo.
	---------------------------
	paramaters.
	query: A string with the format of the dot syntax used in mongo. Ex: 'Agricultura.Culturas Ppermanentes.Abacaxi.Área Colhida'
	city: String with the name of a city part of Rio Grande do Sul state.
	"""
	docs = database.collections.find({f'{query}.nome' : city}, {'_id': 0, f'{query}.$': 1})
	document = list(docs)
	value = recursive(document[0])
	return value

def recursive(dicionary):
	"""
	Walk inside a nested dictionary until it gets to the final value.
	-----------------------------------
	parameter.
	dictionary: Nested dictionary
	"""
	for key, value in dicionary.items():
		if isinstance(value, dict):
			return recursive(value)
		else:
			return value[0]

