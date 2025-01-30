# Implementação de conexão com o MongoDB

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

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


# Função assíncrona para consultar usuário por ID
async def consulta(id_mongo):
    try:
        resultado = await colecao_usuarios.find_one({"_id": ObjectId(id_mongo)})
        return resultado
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None


# Executar apenas se for o script principal
if __name__ == "__main__":
    async def main():
        nome = "João"
        email = "joao@gmail.com"
        age = 34

        # Inserir um usuário no banco
        # id_inserido = await inclusao(nome, email, age)

        # Consultar o usuário pelo ID gerado
        id_inserido = "679bd1919f912ee5ce06dff8"
        resultado = await consulta(id_inserido)

        if resultado:
            print(f"Nome do usuário: {resultado['nome']}")
            print(f"Email do usuário: {resultado['email']}")
            print(f"Idade do usuário: {resultado['age']}")
        else:
            print("Usuário não encontrado.")

    asyncio.run(main())  # Executa as funções assíncronas