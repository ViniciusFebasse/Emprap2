import requests
from decouple import config

DOMAIN = config('DOMAIN')
PORT_API = config('PORT_API')

# URL da API
url = f"http://{DOMAIN}:{PORT_API}/usuarios/"

# Dados que serão enviados para a API
usuarios = [
    {"nome": "1623", "email": "lucas@email.com", "age": 30},
    {"nome": "1624", "email": "jonatas@email.com", "age": 25}
]

# Enviando a requisição POST para a API
response = requests.post(url, json=usuarios)

# Exibindo a resposta da API
if response.status_code == 200:
    print("Resposta da API:", response.json())
else:
    print(f"Erro {response.status_code}: {response.text}")
