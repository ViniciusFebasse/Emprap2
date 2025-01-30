# Consumidor de mensagens do RabbitMQ

import pika
import asyncio  # Para rodar a função assíncrona
from decouple import config
from mongo import consulta  # Importando a função assíncrona
from mysql_db import main

fila = f"{config('FILA')}"
DOMAIN = config('DOMAIN')

# Criar um loop de eventos global para evitar o erro "Event loop is closed"
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


# Função que processa as mensagens recebidas
def callback(ch, method, properties, body):
    id_mongo = body.decode()
    print(f"📨 Mensagem recebida da fila: {id_mongo}")

    try:
        resultado = loop.run_until_complete(consulta(id_mongo))
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        resultado = None  # Garante que não cause erro ao acessar `None`

    if resultado:
        print(f"Resultado da consulta no MongoDB: {resultado}")

        nome = resultado.get('nome')
        email = resultado.get('email')
        age = resultado.get('age')

        print(f"Nome do usuário: {nome}")
        print(f"Email do usuário: {email}")
        print(f"Idade do usuário: {age}")

        # Inserindo no MySQL
        main(nome=nome, email=email, age=age)
    else:
        print("⚠️ Usuário não encontrado no MongoDB.")

    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma que a mensagem foi processada


# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(DOMAIN))
channel = connection.channel()

# Garantir que a fila existe
channel.queue_declare(queue=fila, durable=True)

# Consumir mensagens da fila
channel.basic_consume(queue=fila, on_message_callback=callback)

print("🎧 Aguardando mensagens. Pressione CTRL+C para sair.")
channel.start_consuming()
