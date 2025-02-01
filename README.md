# API de criação de usuários
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Desenvolvedor
- Vinícius Ferreira Bandeira Serra

## Definições
- LINGUAGEM DE PROGRAMAÇÃO: Python 3.11
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

## Diretórios físicos
O projeto é constituído dos seguintes diretórios:
- api: diretório que contém o arquivo principal que contém a API construída com FastAPI
- databases: diretório que contém o arquivo que encapsula as operações com o MongoDB e MySQL
- logs: diretório que contém o arquivo que encapsula as operações de registro de logs em um arquivo txt, assim como o
próprio arquivo de logs
- rabbit_mq: diretório que contém os arquivos que encapsulam as operações de registro na fila do RabbitMQ e o consumer
- testes: diretório que contém o arquivo que realiza os testes unitários

## Arquivos físicos
O projeto é constituído dos seguintes arquivos:
- api/api.py: arquivo principal que contém a API construída com FastAPI
- databases/mongo.py: arquivo que encapsula as operações com o MongoDB
- rabbit_mq/filas.py: arquivo que encapsula as operações de registro na fila do RabbitMQ
- rabbit_mq/consumer.py: arquivo que contém o consumer que processa a fila do RabbitMQ
- databases/mysql_db.py: arquivo que encapsula as operações com o MySQL
- logs/registra_logs.py: arquivo que encapsula as operações de registro de logs em um arquivo txt
- logs/log.txt: arquivo que contém os logs de sucesso e falha
- testes/tests.py: arquivo que contém os testes unitários
- requirements.txt: arquivo que contém as bibliotecas utilizadas
- README.md: arquivo que contém a documentação do projeto
- .env: arquivo que contém as variáveis de ambiente
- docker-compose.yml: arquivo que contém a configuração do Docker

## Fluxo de Execução sem Docker (apenas para instrução, o projeto está configurado com Docker)
- O arquivo api/api.py deve ser executado com o comando: ```unicorn api.api:app --reload``` para rodar a API
- O arquivo rabbit_mq/consumer.py deve ser executado com o comando: ```python rabbit_mq/consumer.py``` para rodar o consumer
- O arquivo testes/tests.py deve ser executado com o comando: ```python testes/tests.py``` para rodar os testes unitários
- Quando a requisição de testes/tests.py for recebida, a API processa os dados e os persiste no MongoDB.
- Tendo havido sucesso na geração do registro no Mongo, o id do usuário é enviado para a fila do RabbitMQ pelo próprio 
api/api.py
- O rabbit_mq/consumer.py que monitora as mensagens, processa o id e faz o registro no MySQL
- Cada operação de sucesso ou falha é registrada no arquivo log.txt

## Utilização com Docker Compose
- Inicialize o serviço do Docker Desktop no PC
- Abra o CMD
- Vá na pasta raíz do projeto
- Rode o comando: ```docker-compose down; docker-compose up --build --remove-orphans``` para subir o container
- Aguarde a finalização do processo
- O RabbitMq está disponível em: http://localhost:15673/#/
- A API está disponível em: http://localhost:8000/
- A documentação da API estará disponível em http://localhost:8000/docs
- As requisições para inserção de usuários devem ser do tipo POST, para tanto
  - Acesse o Docker Desktop > Containers > embrap2 > fastapi_app > Exec
  - Digite o comando: ```python testes/tests.py``` para rodar os testes unitários
  - Acompanhe as mensagens na URL do RabbitMQ
  - Acesse Docker Desktop > Containers > embrap2 > maysql_app > Exec
  - Digite o comando: ```mysql -u root -p``` e a senha: root
  - Digite o comando: ```use embrap2;``` para acessar o database
  - Digite o comando: ```select * from users;``` para visualizar os registros
