"""
Clean the data.
"""

char_to_replace = {'.': ' ',
				   '(': '',
				   ')': '',
				   ',': ' ',
				   '>': 'Maior que ',
				   '<': 'Menor que ',
				   '  ': ' '}

def clean_keys(keys_list):  
	"""
	Clean the keys in the dictionary and the name of the json files.
	--------------------------------------
	keys_list: List conatining the names of the keys in a nested dictionary.
	"""               
	keys = []
	for key in keys_list:
		for k, v in char_to_replace.items():
			key = key.replace(k, v)
		keys.append(key)
	return keys