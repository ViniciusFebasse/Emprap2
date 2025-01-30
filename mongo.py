from motor.motor_asyncio import AsyncIOMotorClient

# URL de conexão ao MongoDB
MONGO_URL = "mongodb://localhost:27017"

# Conectar ao MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client["Embrap2"]  # Nome do banco de dados
colecao_usuarios = db["uploads"]  # Nome da coleção (equivalente a tabela)
