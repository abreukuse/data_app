"""
Query data from mongodb.
"""

import pymongo
import os
from dotenv import load_dotenv

def get_env_variables():
    load_dotenv()
    return (os.getenv("USUARIO"),
            os.getenv("SENHA"),
            os.getenv("CLUSTER"))

# local_connection = 'mongodb://localhost:27017/'
# remote_connection = os.environ['MONGODB_URI'] # Access heroku config vars
usuario, senha, cluster = get_env_variables()
myclient = pymongo.MongoClient(f"mongodb+srv://{usuario}:{senha}@{cluster}.mlrrx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = myclient['fee_database']

def find_document(query, cities): 
    """
    Find the document from the collections in mongo.
    ---------------------------
    paramaters.
    query: A string with the format of the dot syntax used in mongo. Ex: 'Agricultura.Culturas Ppermanentes.Abacaxi.Área Colhida'
    city: String with the name of a city part of Rio Grande do Sul state.
    """
    # docs = database.collections.find({f'{query}' : {'$elemMatch': {'$or': [{'nome':'Caxias do Sul'}, {'nome':'Vacaria'}]}}}, {'_id': 0, f'{query}.$': 1})
    documents = []
    for city in cities:
        search = database.collections.find({f'{query}.nome' : city}, {'_id': 0, f'{query}.$': 1})
        document = list(search)[0]
        documents.append(document)
    
    values = []
    for document in documents:
        value = recursive(document=document)
        values.append(value)
    return values


def recursive(document):
    """
    Walk inside a nested dictionary until it gets to the final value.
    -----------------------------------
    parameter.
    dictionary: Nested dictionary
    """
    for key, value in document.items():
        if isinstance(value, dict):
            return recursive(value)
        else:
            return value[0]
