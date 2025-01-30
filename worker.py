import motor.motor_asyncio
import pymysql
import pika
import json
import logging

# Configuração do MongoDB
MONGO_URI = "mongodb://mongo:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["fastapi_db"]
collection = db["uploads"]

# Configuração do MySQL
MYSQL_CONFIG = {
    "host": "mysql",
    "user": "root",
    "password": "root",
    "database": "fastapi_db"
}

# Configuração do RabbitMQ
RABBITMQ_HOST = "rabbitmq"
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue="json_queue")

# Configuração de logs
logging.basicConfig(filename="logs/worker.log", level=logging.INFO)

def salvar_no_mysql(users):
    """Salva usuários no MySQL"""
    conn = pymysql.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    for user in users:
        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
            (user["name"], user["email"], user["age"])
        )

    conn.commit()
    conn.close()
    logging.info(f"{len(users)} usuários inseridos no MySQL")

def processar_mensagem(ch, method, properties, body):
    """Processa mensagens do RabbitMQ"""
    mongo_id = body.decode()
    document = collection.find_one({"_id": mongo_id})

    if document:
        salvar_no_mysql(document["data"])
        logging.info(f"Processado MongoDB ID {mongo_id}")
    else:
        logging.error(f"Erro ao processar MongoDB ID {mongo_id}")

channel.basic_consume(queue="json_queue", on_message_callback=processar_mensagem, auto_ack=True)
channel.start_consuming()
