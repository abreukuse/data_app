import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Rio_Grande_do_Sul"
print('Getting response from the Wikipedia page.')
response = requests.get(url)

print('Parsing the html.')
soup = BeautifulSoup(response.text, 'html.parser')
items = soup.find_all('td', attrs={'style': 'text-align:left;'})

print('Putting all the cities in a list.')
cities = [item.text.strip() for item in items]

print('Saving the list in a txt file.')
with open('cities_RS.txt', 'w', encoding='latin1') as output:
    output.write(str(cities))