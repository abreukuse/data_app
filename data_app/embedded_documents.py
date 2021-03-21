"""
Create a nested dictionary containing all the keys available.
And also some of these fuctions will be used by others parts of the application.
"""

from functools import reduce
import os
import json
from tqdm import tqdm
from config import DICTIONARY_MASTER, PATH_PREPROCESSED_DATA

def nested_keys(keys, value):
    """
    Create a nested dictionary from a list.
    _________________________________________
    keys: list which each item will be a key in a nested dictionary
    value: value to be included in the last key
    """
    new_dict = current = {}
    last_index = keys.index(keys[-1])

    if not len(set(keys)) < len(keys):
        for name in keys:
            current_index = keys.index(name)
            current[name] = {} if current_index != last_index else value
            current = current[name]
        return new_dict
    else:
        print(f'{keys} has equal values')


def merge(a, b, path=None):
    """
    Merges dict b into dict a
    _________________________
    a and b: python dictionaries
    """
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a     

def get_all_keys(dictionary, empty_list):
    """
    Get all keys from the dictionary passed
    ______________________________________
    dictionary: a nested python dictionary
    empty_list: a simple empty list
    """
    for k, v in dictionary.items():
        if isinstance(v, dict):
            empty_list.append(k)
            get_all_keys(v, empty_list)
        else:
            empty_list.append(k)   


def main():
    """Create a nested dictionary containing all the keys available from the json files."""
    storage = []
    path = PATH_PREPROCESSED_DATA
    files = os.listdir(path)
    try:
        for file in tqdm(files):
            with open(path + file, 'r', encoding='latin1') as json_file:
                document = json.load(json_file)

            keys_from_document = []
            get_all_keys(dictionary=document, empty_list=keys_from_document)
            nested_dictionary = nested_keys(keys=keys_from_document, value=None)
            storage.append(nested_dictionary)

        dictionary_master = reduce(merge, storage)
        with open(DICTIONARY_MASTER, 'w') as output:
            json.dump(dictionary_master, output)

    except Exception as e:
        print(f'{e}\n{file}')


if __name__ == '__main__':
    main()
