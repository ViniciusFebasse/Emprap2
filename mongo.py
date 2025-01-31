# Implementação de conexão com o MongoDB

import asyncio
import time

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from registra_log import registra_log
import datetime as dt

data_agora = dt.datetime.now()
data_agora = data_agora.strftime("%Y-%m-%d %H:%M:%S")

# URL de conexão ao MongoDB
MONGO_URL = "mongodb://localhost:27017"

# Conectar ao MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client["Embrap2"]  # Nome do banco de dados
colecao_usuarios = db["uploads"]  # Nome da coleção (equivalente a tabela)


# Função assíncrona para testar a inserção
async def inclusao(nome, email, age):
    try:
        usuario_teste = {"nome": nome, "email": email, "age": age}

        response = await colecao_usuarios.insert_one(usuario_teste)
        id_mongo = str(response.inserted_id)
        registra_log(log=f"Usuário {nome} registrado com sucesso no MongoDB", data_hora=data_agora)
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        registra_log(log=f"Erro ao inserir usuário no MongoDB", data_hora=data_agora)
        id_mongo = None

    return id_mongo


# Função assíncrona para consultar usuário por ID
async def consulta(id_mongo):
    try:
        resultado = await colecao_usuarios.find_one({"_id": ObjectId(id_mongo)})
        registra_log(log=f"Usuário de id {id_mongo} consultado com sucesso no MongoDB", data_hora=data_agora)
        return resultado
    except Exception as e:
        registra_log(log=f"Erro ao consultar usuário de id {id_mongo} no MongoDB", data_hora=data_agora)
        return None


# Executar apenas se for o script principal
if __name__ == "__main__":
    async def main():
        nome = [{time.sleep(1)}]
        email = "1445@gmail.com"
        age = 34

        # Inserir um usuário no banco
        id_inserido = await inclusao(nome, email, age)
        print(f"ID do usuário inserido: {id_inserido}")

        # Consultar o usuário pelo ID gerado
        # id_inserido = {[time.sleep(1)]}
        # resultado = await consulta(id_inserido)

        # if resultado:
        #     print(f"Nome do usuário: {resultado['nome']}")
        #     print(f"Email do usuário: {resultado['email']}")
        #     print(f"Idade do usuário: {resultado['age']}")
        # else:
        #     print("Usuário não encontrado.")

    asyncio.run(main())  # Executa as funções assíncronas