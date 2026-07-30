FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Copia o código fonte
COPY . .

EXPOSE 8000