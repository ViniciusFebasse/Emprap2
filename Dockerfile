# Usa a imagem oficial do Python 3.11
FROM python:3.11

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia apenas o arquivo de dependências para instalar primeiro
COPY requirements.txt /tmp/requirements.txt

# Atualiza o pip e instala os pacotes no sistema global do contêiner
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 8000

# Executa o FastAPI com Uvicorn
CMD ["sh", "-c", "sleep 10 && uvicorn api.api:app --host 0.0.0.0 --port 8000 --reload"]
