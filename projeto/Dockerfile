# Usa uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# --- Configuração para o Selenium (Chrome) ---
# Atualiza o sistema e instala dependências básicas
# Em seguida, baixa o .deb oficial do Chrome e instala diretamente
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# --- Instalação das dependências Python ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Finalização ---
COPY . .

# Define o comando padrão
ENTRYPOINT ["python"]