"""
Import all the json files as documents to MongoDB.
"""

import pymongo
import json
import os
from tqdm import tqdm
from data_app.config import PATH_PREPROCESSED_DATA

def import_data_to_mongo():
    # local_connection = 'mongodb://localhost:27017/'
    remote_connection = os.environ['MONGODB_URI']
    myclient = pymongo.MongoClient(remote_connection)
    database = myclient['fee_database']

    collections = database['collections']

    data_path = PATH_PREPROCESSED_DATA
    files = os.listdir(data_path)

    json_files = []
    for file in tqdm(files):
    	with open(data_path / file, 'r') as json_file:
    		json_files.append(json.load(json_file))

    print(f'Insert {len(json_files)} files.')

    database.collections.insert_many(json_files)

if __name__ == '__main__':
    import_data_to_mongo()