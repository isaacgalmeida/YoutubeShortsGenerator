# Dockerfile
FROM python:3.9-slim

# Instala dependências do sistema para ffmpeg, ImageMagick e bibliotecas gráficas necessárias
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libsm6 \
    libxext6 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia o requirements.txt e instala as dependências Python (incluindo python-dotenv)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o container
COPY . .

# Comando padrão para executar o aplicativo
CMD ["python", "app.py"]
