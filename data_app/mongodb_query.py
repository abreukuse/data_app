import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
database = myclient['fee_database']

# Emprego-Número de Estabelecimentos-Com Vínculos Ativos-CNAE 2 0 Seção-01 Agricultura Pecuária Prod fl Pesca Aqüicultura
inputs = ['Emprego',
		  'Número de Estabelecimentos',
		  'Com Vínculos Ativos',
		  'CNAE 2 0 Seção',
		  '01 Agricultura Pecuária Prod fl Pesca Aqüicultura']

query = '.'.join(inputs)
city = 'São Leopoldo'

def recursive(dicionary):
	for key, value in dicionary.items():
		if isinstance(value, dict):
			return recursive(value)
		else:
			return value[0]

def find_document():
	try:
		docs = database.collections.find({f'{query}.nome' : city}, {'_id': 0, f'{query}.$': 1})
		document = list(docs)
		print(query)
		print(len(document))
		value = recursive(document[0])
		print(value)			
	except:
		print('Documento não encontrado')

if __name__ == '__main__':
	find_document()