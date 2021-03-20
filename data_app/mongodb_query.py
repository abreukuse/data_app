import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
database = myclient['fee_database']

def find_document(query, city): 
    docs = database.collections.find({f'{query}.nome' : city}, {'_id': 0, f'{query}.$': 1})
    document = list(docs)
    print('*****DOCUMENT*****', document)
    value = recursive(document[0])
    return value

def recursive(dicionary):
	for key, value in dicionary.items():
		if isinstance(value, dict):
			return recursive(value)
		else:
			return value[0]

