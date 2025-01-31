# Execução de testes do processo de integração

import requests
from decouple import config

DOMAIN = config('DOMAIN')
PORT_API = config('PORT_API')

# URL da API
url = f"http://{DOMAIN}:{PORT_API}/usuarios/"

nome_novo_usuario = '1611'

# Dados que serão enviados para a API
usuarios = [
    {"nome": nome_novo_usuario, "email": f"{nome_novo_usuario}@email.com", "age": 30},
]

# Enviando a requisição POST para a API
response = requests.post(url, json=usuarios)

# Exibindo a resposta da API
if response.status_code == 200:
    print("Resposta da API:", response.json())
else:
    print(f"Erro {response.status_code}: {response.text}")
