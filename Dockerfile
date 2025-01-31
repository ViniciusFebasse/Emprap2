# Usa a imagem oficial do Python 3.11
FROM python:3.11

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para dentro do contêiner
COPY . /app

# Atualiza o pip e instala os pacotes do requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Verifica se o uvicorn está corretamente instalado
RUN pip show uvicorn

# Expor a porta 8000 para a API
EXPOSE 8000

# Executa o FastAPI com Uvicorn
CMD ["python", "-m", "uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
