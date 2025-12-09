# 🐍 Desafio Técnico - Desenvolvedor Python

Bem-vindo à solução do desafio técnico para a vaga de Desenvolvedor Python. Este projeto reúne scripts de automação, *web scraping*, estruturas de dados e conceitos de infraestrutura em nuvem, totalmente containerizados para garantir portabilidade e reprodutibilidade, conforme solicitado nas instruções do teste.

## 📋 Visão Geral do Projeto

O objetivo deste projeto é demonstrar competências em:
* **Web Scraping:** Extração de dados complexos utilizando `Requests`, `Scrapy` e `Selenium`.
* **Automação:** Simulação de fluxos de pedidos e lógica de carrinho de compras.
* **Engenharia de Software:** Uso de Docker, *Logging* e testes unitários.
* **Estruturas de Dados:** Implementação e manipulação de árvores.
* **Cloud (AWS):** Conceitos fundamentais de rede e segurança.

## 🛠️ Stack Tecnológico

* **Linguagem:** Python 3.6+
* **Containerização:** Docker
* **Bibliotecas Principais:** `scrapy`, `requests`, `selenium`, `pynacl`.
* **Observabilidade:** Módulo nativo `logging`.

---

## 🚀 Instalação e Configuração

Conforme os requisitos, não é necessária a instalação local do interpretador Python. Todo o ambiente é gerenciado via Docker.

1.  **Construir a Imagem:**
    Execute o comando abaixo na raiz do projeto para criar a imagem com todas as dependências (incluindo drivers para o Selenium):

    ```bash
    docker build -t teste-python .
    ```

---

## 💻 Guia de Execução (Passo a Passo)

Abaixo estão os comandos para executar cada questão isoladamente. Os arquivos gerados (JSONs) serão salvos automaticamente na sua pasta local (graças ao volume `-v`).

### 1️⃣ Questão 1: Scraping "Compra Agora"
Script que realiza login seguro e extrai informações de produtos.
* **Técnica:** Utiliza a biblioteca `Requests` para navegação HTTP rápida e `PyNaCl` para criptografia de senha, conforme exigido no teste[cite: 22, 24].
* **Comando:**
    ```bash
    docker run -v $(pwd):/app teste-python python q1_compra_agora.py
    ```
* **Resultado:** Gera o arquivo `produtos.json` (Nota: devido às credenciais antigas do teste, o JSON pode ser gerado vazio, comprovando a tentativa de conexão real).

### 2️⃣ Questão 2: Consulta Servimed (Scrapy)
Spider desenvolvido com Scrapy para consultar o status de faturamento de um pedido específico.
* **Uso:** Recebe o ID do pedido como argumento na linha de comando.
* **Comando (Exemplo para o pedido 511082):**
    ```bash
    docker run -v $(pwd):/app teste-python python q2_servimed_runner.py 511082
    ```
* **Resultado:** Gera um JSON com os campos Motivo, Itens e Quantidade Faturada.

### 3️⃣ Questão 3: Automação CooperTotal
* **Status:** Questão anulada conforme alinhamento com a recrutadora (Julia).
* **Arquivo:** Consulte `Questao3.txt` para mais detalhes.

### 4️⃣ Questão 4: Engenharia Reversa (FTP)
A solução para o desafio de conexão FTP e descoberta de credenciais encontra-se documentada no arquivo de texto solicitado.
* **Arquivo:** Consulte `Questao4.txt` na raiz deste repositório contendo host, usuário, senha e conteúdo do arquivo encontrado.

### 5️⃣ Questão 5: Estrutura de Dados (Árvore)
Implementação de uma estrutura de **Árvore** em Python. A solução inclui a classe da árvore e testes unitários que demonstram a inserção e busca de nós.
* **Comando (Rodar Testes):**
    ```bash
    docker run teste-python python -m unittest discover
    ```
* **Explicação Técnica:** A árvore foi implementada permitindo que cada nó (`Node`) possua uma lista dinâmica de filhos, adequada para representar hierarquias não-binárias, com métodos de travessia para localização de dados. A lógica e os testes foram separados em arquivos distintos (`q5_arvore.py` e `test_q5_arvore.py`) seguindo boas práticas.

### 6️⃣ Questão 6: Selenium (Quotes to Scrape)
Bot que busca citações de um autor específico, extrai suas tags e navega para a página de biografia ("About").
* **Uso:** Recebe o nome do autor entre aspas como argumento (Ex: "J.K. Rowling").
* **Comando:**
    ```bash
    docker run -v $(pwd):/app teste-python python q6_selenium.py "J.K. Rowling"
    ```
* **Nota:** O navegador roda em modo *headless* (sem interface gráfica) dentro do container para compatibilidade com Docker.

### 7️⃣ Questão 7: Infraestrutura AWS
Explicação teórica sobre a relação entre VPC, Subnets e Security Groups.
* **Localização:** A resposta completa encontra-se no arquivo `Questao7_AWS.md`.

## 📦 Estrutura do Repositório

```text
.
├── README.md                 # Documentação atualizada
└── projeto/                  # Pasta com os códigos
    ├── Dockerfile            # Mantido com Chrome para a Q6
    ├── requirements.txt      # Atualizado
    ├── Questao4.txt          # Resposta Q4
    ├── Questao3.txt          # Aviso de anulação da Q3 (NOVO)
    ├── q1_compra_agora.py    # Seu código novo (Requests + Pynacl)
    ├── q2_servimed_scrapy.py # Crawler Scrapy
    ├── q5_arvore.py          # Árvore
    ├── test_q5_arvore.py     # Testes
    └── q6_selenium.py        # Bot Selenium (J.K. Rowling)
