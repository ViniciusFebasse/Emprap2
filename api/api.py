# Arquivo de definição da API com FastAPI

from typing import List
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from databases.mongo import inclusao
from rabbit_mq.filas import registrar_id_mongo

from logs.registra_log import registra_log
from parametros import busca_data_agora

data_agora = busca_data_agora()

# Definindo o modelo do usuário
class Usuario(BaseModel):
    nome: str
    email: str
    age: int

# Inicializando a aplicação FastAPI
app = FastAPI()

# Captura erros de validação e retorna uma mensagem personalizada
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,  # Código 400 para erro de requisição inválida
        content={"message": "As chaves de cada registro precisam ser as mesmas e devem ser apenas nome, email e age"},
    )

# Endpoint para receber uma lista de usuários
@app.post("/usuarios/")
async def criar_usuarios(usuarios: List[Usuario]):
    registra_log(log="API de criação de usuários requisitada", data_hora=data_agora)
    tipo_dados = type(usuarios)

    # Verifica o tipo de dados
    if tipo_dados == list:
        # Verifica se as chaves estão corretas
        qtd_usuarios_criados = 0

        for usuario in usuarios:
            # Verifica os campos do main.Usuario
            if not hasattr(usuario, "nome") or not hasattr(usuario, "email") or not hasattr(usuario, "age"):
                mensagem = "Erro no processamento da API: os dados dos usuário devem possuir as chaves nome, email e age."
                print(mensagem)
                registra_log(log=mensagem, data_hora=data_agora)
                return mensagem

            else:
                resultado = await inclusao(nome=usuario.nome, email=usuario.email, age=usuario.age)

                id_mongo = resultado

                if id_mongo:
                    # Enviar ID do MongoDB para a fila do RabbitMQ
                    response = registrar_id_mongo(id_mongo)
                    qtd_usuarios_criados += 1
                else:
                    mensagem = "Erro ao inserir usuário no MongoDB."
                    print(mensagem)
                    return mensagem

        mensagem = f"Foram recebidos {len(usuarios)} usuários na listagem"
        print(mensagem)
        registra_log(log=mensagem, data_hora=data_agora)

        return {"message": mensagem}
    else:
        mensagem = "Erro: os dados enviados não são uma lista de usuários."
        registra_log(log=mensagem, data_hora=data_agora)
        print(mensagem)
        return "Erro: os dados enviados não são uma lista de usuários."


# Bloquear método get
@app.get("/usuarios/")
def get_usuarios():
    return {"message": "Método GET não permitido. Use o método POST para enviar dados de usuários."}

@app.get("/")
def home():
    return {"message": "API para cadastro de usuários. Acesse /docs para ver a documentação."}
