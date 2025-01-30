from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Definindo o modelo do usuário
class Usuario(BaseModel):
    nome: str
    email: str
    idade: int

# Inicializando a aplicação FastAPI
app = FastAPI()

# Endpoint para receber uma lista de usuários
@app.post("/usuarios/")
def criar_usuarios(usuarios: List[Usuario]):
    print("Usuários recebidos:", usuarios)
    return usuarios
