import pika
from decouple import config


def registrar_id_mongo(id_mongo):
    try:
        DOMAIN = f"{config('DOMAIN')}"
        fila = "ids_mongo"

        # Conectar ao RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(DOMAIN))
        channel = connection.channel()

        print(connection)

        # Declarar a fila (caso ainda não exista)
        channel.queue_declare(queue=fila, durable=True)  # `durable=True` mantém a fila após reinícios

        # Mensagem a ser enviada
        mensagem = id_mongo

        # Publicar a mensagem na fila
        channel.basic_publish(
            exchange='',
            routing_key=fila,  # Nome da fila
            body=mensagem,
            properties=pika.BasicProperties(
                delivery_mode=2  # Garante que a mensagem será persistida
            )
        )

        print(f"📩 Mensagem enviada para a fila: {mensagem}")

        # Fechar a conexão
        connection.close()

        return "Mensagem enviada com sucesso para a fila."
    except Exception as e:
        return f"Erro ao enviar mensagem para a fila: {e}"


if __name__ == "__main__":
    registrar_id_mongo("1234567890")