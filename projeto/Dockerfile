# Usa uma imagem base oficial do Python (atende ao requisito Python 3.6+ )
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# --- Configuração para o Selenium (Chrome) ---
# Instala dependências do sistema para o Chrome e o próprio Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# --- Instalação das dependências Python ---
# Copia o arquivo de requisitos para dentro do container
COPY requirements.txt .

# Instala as bibliotecas Python sem cache para deixar a imagem mais leve
RUN pip install --no-cache-dir -r requirements.txt

# --- Finalização ---
# Copia todos os scripts do seu projeto para a pasta /app do container
COPY . .

# Define o comando padrão para executar scripts Python
# Isso permite que você passe o nome do script como argumento ao rodar o container
ENTRYPOINT ["python"]