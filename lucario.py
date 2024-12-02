from concurrent.futures import ThreadPoolExecutor

import requests
import csv

url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"

response = requests.get(url)
data = response.json()

pokemon_list = data['results']

# Rows
def fetch_pokemon_data(pokemon):
    pokemon_url = pokemon['url']
    pokemon_response = requests.get(pokemon_url)
    pokemon_data = pokemon_response.json()

    return[
        pokemon_data['base_experience'],
        pokemon_data['height'],
        pokemon_data['name'],
        pokemon_data['weight']
    ]


# Header
with open('pokemon_data.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['base_experience', 'height', 'name', 'weight'])

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_pokemon_data, pokemon_list)
        for result in results:
            writer.writerow(result)

        

print('Dados salvos com sucesso!')