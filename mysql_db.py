from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Definir a URL de conexão com o MySQL
DATABASE_URL = "mysql+mysqlconnector://root:JCeDo1eou#@localhost:3306/embrap2"

# Criar uma base para as classes mapeadas
Base = declarative_base()


# Definir o modelo de dados (tabela 'users')
class User(Base):
    __tablename__ = 'users'

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
        print(f"Tabelas criadas ou verificadas com sucesso no banco '{DATABASE_URL.split('/')[-1]}'.")
    except OperationalError as e:
        print(f"Erro ao conectar ou criar tabelas no banco de dados: {e}")

    return engine


# Função para inserir um usuário na tabela
def inserir_usuario(session, nome, email, idade):
    usuario = User(name=nome, email=email, age=idade)
    session.add(usuario)
    session.commit()
    print(f"Usuário {nome} inserido com sucesso!")


# Função principal
def main():
    # Conectar ao banco e criar a tabela (caso não exista)
    engine = criar_conexao()

    # Criar uma sessão para interagir com o banco
    Session = sessionmaker(bind=engine)
    session = Session()

    # Inserir um usuário como exemplo
    inserir_usuario(session, "João", "joao@example.com", 34)

    session.close()  # Fechar a sessão


if __name__ == "__main__":
    main()
