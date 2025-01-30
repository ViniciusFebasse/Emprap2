import asyncio

from typing import List
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from mongo import inclusao

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
    print("Usuários recebidos:", usuarios)
    tipo_dados = type(usuarios)
    print("Tipo da variável 'usuarios':", tipo_dados)

    # Verifica o tipo de dados
    if tipo_dados == list:
        # Verifica se as chaves estão corretas
        qtd_usuarios_criados = 0

        for usuario in usuarios:
            # Verifica os campos do main.Usuario
            print("Campos do usuário:", usuario.nome, usuario.email, usuario.age)
            if not hasattr(usuario, "nome") or not hasattr(usuario, "email") or not hasattr(usuario, "age"):
                mensagem = "Erro: os dados dos usuário devem possuir as chaves nome, email e age."
                print(mensagem)
                return "Erro: os dados dos usuário devem possuir as chaves nome, email e age."

            else:
                resultado = await inclusao(nome=usuario.nome, email=usuario.email, age=usuario.age)

                print("ID do usuário inserido:", resultado.inserted_id)
                qtd_usuarios_criados += 1

        mensagem = f"Foram recebidos com sucesso {len(usuarios)} usuários na listagem e {qtd_usuarios_criados} usuários foram criados no banco de dados."
        print(mensagem)

        return {"message": mensagem}
    else:
        mensagem = "Erro: os dados enviados não são uma lista de usuários."
        print(mensagem)
        return "Erro: os dados enviados não são uma lista de usuários."


# Bloquear método get
@app.get("/usuarios/")
def get_usuarios():
    return {"message": "Método GET não permitido. Use o método POST para enviar dados de usuários."}

@app.get("/")
def home():
    return {"message": "API para cadastro de usuários. Acesse /docs para ver a documentação."}
