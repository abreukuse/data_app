char_to_replace = {'.': ' ',
                   '(': '',
                   ')': '',
                   ',': ' ',
                   '>': 'Maior que ',
                   '<': 'Menor que ',
                   '  ': ' '}

def clean_keys(keys_list):                 
    keys = []
    for key in keys_list:
        for k, v in char_to_replace.items():
            key = key.replace(k, v)
        keys.append(key)
    return keys