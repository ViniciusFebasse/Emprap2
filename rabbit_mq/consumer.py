# Consumidor de mensagens do RabbitMQ
import time

import pika
import asyncio
import traceback
from decouple import config

import os
import sys
# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    print("Importando módulos...", flush=True)
    from databases.mongo import consulta
    from databases.mysql_db import main
    from parametros import busca_data_agora
except:
    traceback.print_exc()
    print("Erro ao importar módulos.", flush=True)

    from app.databases.mongo import consulta
    from app.databases.mysql_db import main
    from app.parametros import busca_data_agora

data_agora = busca_data_agora()

fila = f"{config('FILA')}"
DOMAIN = config('DOMAIN')
SERVICE_RABBIT = config('SERVICE_RABBIT')

# Criar um loop de eventos global para evitar o erro "Event loop is closed"
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


# Função que processa as mensagens recebidas
def callback(ch, method, properties, body):
    id_mongo = body.decode()

    try:
        resultado = loop.run_until_complete(consulta(id_mongo))
    except Exception as e:
        resultado = None

    if resultado:
        nome = resultado.get('nome')
        email = resultado.get('email')
        age = resultado.get('age')

        # Inserindo no MySQL
        main(nome=nome, email=email, age=age)

    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma que a mensagem foi processada


# Conectar ao RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=SERVICE_RABBIT, port=config('PORT_MQ')))
except:
    time.sleep(10)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=SERVICE_RABBIT, port=5672))

channel = connection.channel()

# Garantir que a fila existe
channel.queue_declare(queue=fila, durable=True)

# Consumir mensagens da fila
channel.basic_consume(queue=fila, on_message_callback=callback)

print("🎧 Aguardando mensagens. Pressione CTRL+C para sair.")
channel.start_consuming()
