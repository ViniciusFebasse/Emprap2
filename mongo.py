import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# URL de conexão ao MongoDB
MONGO_URL = "mongodb://localhost:27017"

# Conectar ao MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client["Embrap2"]  # Nome do banco de dados
colecao_usuarios = db["uploads"]  # Nome da coleção (equivalente a tabela)


# Função assíncrona para testar a inserção
async def inclusao(nome, email, age):
    usuario_teste = {"nome": nome, "email": email, "age": age}

    resultado = await colecao_usuarios.insert_one(usuario_teste)
    print(f"Usuário inserido com ID: {resultado.inserted_id}")

    return resultado


# Executar apenas se for o script principal
if __name__ == "__main__":
    nome = "João"
    email = "joao@gmail.com"
    age = 34
    resultado = asyncio.run(inclusao(nome=nome, email=email, age=age))  # Executa a função assíncrona
    print(resultado)
