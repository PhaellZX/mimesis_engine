# Usamos uma imagem Python leve
FROM python:3.12-slim

# Instala o stockfish diretamente dos repositórios oficiais do Debian/Ubuntu
# Isso evita problemas de compatibilidade com o binário que você baixou
RUN apt-get update && apt-get install -y \
    stockfish \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Variável de ambiente para o Flask e para o caminho do Stockfish
# No Linux (via apt), o stockfish fica em /usr/games/stockfish
ENV STOCKFISH_PATH=/usr/games/stockfish
ENV FLASK_APP=app.py

# Porta que o Render e o Docker vão usar
EXPOSE 5000

# Comando para rodar com Gunicorn (Produção)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]