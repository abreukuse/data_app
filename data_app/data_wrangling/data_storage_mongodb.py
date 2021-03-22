"""
Import all the json files as documents in MongoDB.
"""

import pymongo
import json
import os
from tqdm import tqdm
from config import PATH_PREPROCESSED_DATA

def import_data_to_mongo():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    database = myclient['fee_database']

    collections = database['collections']

    data_path = PATH_PREPROCESSED_DATA
    files = os.listdir(data_path)

    json_files = []
    for file in tqdm(files):
    	with open(data_path + file, 'r') as json_file:
    		json_files.append(json.load(json_file))

    print(f'Insert {len(json_files)} files.')

    database.collections.insert_many(json_files)

if __name__ == '__main__':
    import_data_to_mongo()