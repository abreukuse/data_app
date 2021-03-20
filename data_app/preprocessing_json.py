"""
Preprocess the data in order to insert them in a mongodb database.
"""

import os
from zipfile import ZipFile
from tqdm import tqdm
import json
from embedded_documents import nested_keys
from clean_keys_names import clean_keys

path_unziped_files = os.getcwd() + '\\unziped_files\\'
download_path = os.getcwd() + '\\download\\'
path_preprocessed_data = os.getcwd() + '\\preprocessed_data\\'

def unzip_files():
    """Unzip all files and store in the unziped_files directory"""
    print(f'Unziped files directory: {path_unziped_files}')
    os.mkdir(path_unziped_files)

    files = os.listdir(download_path)
    print('Extracting files:')
    for file in tqdm(files):
        try:
            with ZipFile(download_path + file, 'r') as zip_object:
                zip_object.extractall(path = path_unziped_files)
        except Exception as e:
            print(f'{e}\n{file}')


def preprocessing_json():
    """Preprocess the data in order to insert them in a mongodb database."""

    # Unzip all the files
    if not os.path.isdir(path_unziped_files):
        unzip_files()

    # Check for the preprocessed_data directory
    if not os.path.isdir(path_preprocessed_data):
        os.mkdir(path_preprocessed_data)

    # Preprocess the data
    files = os.listdir(path_unziped_files)
    for file in tqdm(files):
        try:
            with open(path_unziped_files + file, 'r', encoding='latin1') as json_file:
                data = json.load(json_file)

            # Get the key names and values from each json file
            keys_list = data['variavel'][0]['caminho'].split('/')
            keys_list = [x.strip() for x in keys_list if len(x) > 0]
            
            # Change/clean keys names in each document
            keys = clean_keys(keys_list)
            value = data['unidadesGeograficas']

            # Organize the jsons to be inserted in mongodb
            document = nested_keys(keys=keys, value=value)

            # Store document object
            document_name = '-'.join(keys)
            with open(path_preprocessed_data+document_name+'.json', 'w') as output:
                json.dump(document, output)

        except Exception as e:
            print(f'{e}\n{file}')


if __name__ == '__main__':
    preprocessing_json()