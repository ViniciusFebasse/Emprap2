# API de criação de usuários
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Desenvolvedor
- Vinícius Ferreira Bandeira Serra

## Definições
- LINGUAGEM DE PROGRAMAÇÃO: Python 3.10
- DESCRIÇÃO SUSCINTA: API para criação de usuários, que processa e persiste os dados no MongoDB. Na sequência o id do
usuário é enviado para uma fila no RabbitMQ. Um consumer processa o id e faz o registro no MySQL. Sendo que cada 
operação de sucesso ou falha é registrada em um arquivo txt.
- BIBLIOTECAS UTILIZADAS: estão descritas no arquivo requirements.txt
- DADOS SENSÍVEIS E VARIÁVEIS DE AMBIENTE: definidos no arquivo .env
- SISTEMA OPERACIONAL: Windows 11

## Dependências
- Python 3.11 instalado
- FastAPI instalado
- Download e instalação do RabbitMQ: https://www.rabbitmq.com/docs/install-windows
- Download e instalação do Erlang (necessário para o RabbitMQ): https://www.erlang.org/downloads
- Ativação do Management do RabbitMQ: https://www.rabbitmq.com/docs/management
- Download e instalação do MySQL

## Ativação do Management do RabbitMQ
- vá na pasta de instalação do RabbitMQ, exemplo: (C:\Program Files\RabbitMQ Server\rabbitmq_server-4.0.5\sbin)
- abra o CMD, vá na pasta acima
- rode o comando: rabbitmq-plugins enable rabbitmq_management
- ative o telnet no Windows para verificar a instalação: dism /online /Enable-Feature /FeatureName:TelnetClient
- reinicie o PC
- faça um telnet para verificar a instalação: telnet 127.0.0.1 5672
- abra a página: http://localhost:15672/. Usuário: guest, Senha: guest

## Configuração do MySQL
- comando para acessar o mysql: mysql -u root -p
- crie o database com CREATE DATABASE embrap2; no CMD

# Documentação
Documentação com ReDoc: http://127.0.0.1:8000/redoc
Documentação com Swagger: http://127.0.0.1:8000/docs

## Arquivos físicos
O projeto é constituído dos seguintes arquivos:
- api.py: arquivo principal que contém a API construída com FastAPI
- mongo.py: arquivo que encapsula as operações com o MongoDB
- filas.py: arquivo que encapsula as operações de registro na fila do RabbitMQ
- consumer.py: arquivo que contém o consumer que processa a fila do RabbitMQ
- mysql_db.py: arquivo que encapsula as operações com o MySQL
- registra_logs.py: arquivo que encapsula as operações de registro de logs em um arquivo txt
- log.txt: arquivo que contém os logs de sucesso e falha
- tests.py: arquivo que contém os testes unitários
- requirements.txt: arquivo que contém as bibliotecas utilizadas
- README.md: arquivo que contém a documentação do projeto
- .env: arquivo que contém as variáveis de ambiente
- docker-compose.yml: arquivo que contém a configuração do Docker

## Fluxo de Execução
- O arquivo api.py deve ser executado com o comando: ```unicorn api:app --reload``` para rodar a API
- O arquivo consumer.py deve ser executado com o comando: ```python consumer.py``` para rodar o consumer
- O arquivo tests.py deve ser executado com o comando: ```python tests.py``` para rodar os testes unitários
- Quando a requisição de tests.py for recebida, a API processa os dados e os persiste no MongoDB.
- Tendo havido sucesso na geração do registro no Mongo, o id do usuário é enviado para a fila do RabbitMQ pelo próprio 
api.py
- O consumer.py que monitora as mensagens, processa o id e faz o registro no MySQL
- Cada operação de sucesso ou falha é registrada no arquivo log.txt
