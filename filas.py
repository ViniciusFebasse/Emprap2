# Implementação de função para registrar ID do Mongo na fila do RabbitMQ

import pika
from decouple import config
from registra_log import registra_log
from parametros import busca_data_agora

data_agora = busca_data_agora()

# Registra ID do Mongo na fila do RabbitMQ
def registrar_id_mongo(id_mongo):
    try:
        DOMAIN = f"{config('DOMAIN')}"
        fila = f"{config('FILA')}"

        # Conectar ao RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(DOMAIN))
        channel = connection.channel()

        # Declarar a fila (caso ainda não exista)
        channel.queue_declare(queue=fila, durable=True)  # `durable=True` mantém a fila após reinícios

        # Mensagem a ser enviada
        mensagem = f"ID do usuário no Mongo DB enviado para fila do RabbitMq com sucesso: {id_mongo}"

        # Publicar a mensagem na fila
        channel.basic_publish(
            exchange='',
            routing_key=fila,  # Nome da fila
            body=id_mongo,
            properties=pika.BasicProperties(
                delivery_mode=2  # Garante que a mensagem será persistida
            )
        )

        registra_log(log=mensagem, data_hora=data_agora)

        # Fechar a conexão
        connection.close()

        return mensagem
    except Exception as e:
        mensagem = f"Erro ao enviar mensagem para a fila do RabbitMq: {id_mongo}"
        registra_log(log=mensagem, data_hora=data_agora)
        return mensagem


if __name__ == "__main__":
    registrar_id_mongo("1234567890")