import requests

response = requests.get(f'https://api.gael.cloud/general/public/clima')

response = response.json()

LA = list(filter(lambda city: city["Estacion"] == "Los Ángeles", response))

print(LA[0]["Temp"])