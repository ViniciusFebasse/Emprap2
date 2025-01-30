# Instalações
Instalação do FastAPI: pip install fastapi uvicorn
Instalação do PydanticEmail: pip install pydantic[email]

# Execução
Código para executar a API: uvicorn main:app --reload

# Documentação
Documentação com ReDoc: http://127.0.0.1:8000/redoc
Documentação com Swagger: http://127.0.0.1:8000/docs

# RabbitMQ
Download do Erlang (requisito para o RabbitMq): https://www.erlang.org/downloads
Documentação do RabbitMq: https://www.rabbitmq.com/tutorials/tutorial-one-python
Donwload do RabbitMQ para Windows: https://www.rabbitmq.com/docs/install-windows
Documentação para ativar o Management: https://www.rabbitmq.com/docs/management
- vá na pasta de instalação do RabbitMQ (C:\Program Files\RabbitMQ Server\rabbitmq_server-4.0.5\sbin)
- abra o CMD, vá na pasta acima
- rode o comando: rabbitmq-plugins enable rabbitmq_management
- ative o telnet no Windows para verificar a instalação: dism /online /Enable-Feature /FeatureName:TelnetClient
- reinicie o PC
- faça um telnet para verificar a instalação: telnet 127.0.0.1 5672
- abra a página: http://localhost:15672/. Usuário: guest, Senha: guest

# MySQL
- comando para acessar o mysql: mysql -u root -p
- crie o database com CREATE DATABASE embrap2; no CMD