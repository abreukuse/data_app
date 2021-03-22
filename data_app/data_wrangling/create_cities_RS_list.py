"""
Collect and save, as a txt file, the names of all cities composing the Rio Grande do Sul state.
"""

import requests
from bs4 import BeautifulSoup
from data_app.config import FILES

def get_cities_names():
    url = "https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Rio_Grande_do_Sul"
    print('Getting response from the Wikipedia page.')
    response = requests.get(url)

    print('Parsing the html.')
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('td', attrs={'style': 'text-align:left;'})

    print('Putting all the cities in a list.')
    cities = [item.text.strip() for item in items]

    print('Saving the list in a txt file.')
    save_file_name = FILES / 'cities_RS.txt'
    with open(save_file_name, 'w', encoding='latin1') as output:
        output.write(str(cities))

if __name__ == '__main__':
    get_cities_names()