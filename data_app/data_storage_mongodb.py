import pymongo
import json
import os
from tqdm import tqdm

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
database = myclient['fee_database']

collections = database['collections']

data_path = os.getcwd() + '\\preprocessed_data\\'
files = os.listdir(data_path)

json_files = []
for file in tqdm(files):
	with open(data_path + file, 'r') as json_file:
		json_files.append(json.load(json_file))

print(f'Insert {len(json_files)} files.')

database.collections.insert_many(json_files)