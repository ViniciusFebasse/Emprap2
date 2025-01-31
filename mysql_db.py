# Arquivo para encapsular a lógica de conexão com o banco de dados MySQL e inserção de dados na tabela 'users'.

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from registra_log import registra_log
from decouple import config
from parametros import busca_data_agora

data_agora = busca_data_agora()

# Definir a URL de conexão com o MySQL
DATABASE_URL = config('DATABASE_URL_MYSQL')

# Criar uma base para as classes mapeadas
Base = declarative_base()


# Definir o modelo de dados (tabela 'users')
class User(Base):
    __tablename__ = config('TABLE_MYSQL')

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)


# Função para conectar ao banco de dados e criar a tabela
def criar_conexao():
    engine = create_engine(DATABASE_URL, pool_recycle=3600)

    # Criar as tabelas no banco de dados, caso não existam
    try:
        Base.metadata.create_all(engine)
        mensagem = f"Tabelas criadas ou verificadas com sucesso no MySQL '{DATABASE_URL.split('/')[-1]}'."
        registra_log(log=mensagem, data_hora=data_agora)
    except OperationalError as e:
        mensagem = f"Erro ao conectar ou criar tabelas no banco de dados: {e}"
        registra_log(log=mensagem, data_hora=data_agora)

    return engine


# Função para inserir um usuário na tabela
def inserir_usuario(session, nome, email, idade):
    try:
        usuario = User(name=nome, email=email, age=idade)
        session.add(usuario)
        session.commit()
        mensagem = f"Usuário {nome} inserido com sucesso no MySQL!"
        registra_log(log=mensagem, data_hora=data_agora)

    except Exception as e:
        mensagem = f"Erro ao inserir usuário no MySQL: {e}"
        registra_log(log=mensagem, data_hora=data_agora)


# Função principal
def main(nome, email, age):
    # Conectar ao banco e criar a tabela (caso não exista)
    engine = criar_conexao()

    # Criar uma sessão para interagir com o banco
    Session = sessionmaker(bind=engine)
    session = Session()

    # Inserir um usuário como exemplo
    inserir_usuario(session, nome, email, age)

    session.close()  # Fechar a sessão


if __name__ == "__main__":
    main(nome="Shirley", email="shirley@gmail.com", age=39)
