import requests

# URL da API
url = "http://127.0.0.1:8000/usuarios/"

# Dados que serão enviados para a API
usuarios = [
    {"nome": "Lucas", "email": "lucas@email.com", "age": 30},
    {"nome": "Jônatas", "email": "jonatas@email.com", "age": 25}
]

# Enviando a requisição POST para a API
response = requests.post(url, json=usuarios)

# Exibindo a resposta da API
if response.status_code == 200:
    print("Resposta da API:", response.json())
else:
    print(f"Erro {response.status_code}: {response.text}")
