# 🪄 Mimesis Engine | Chess Intelligence Engine

Mimesis Engine é uma plataforma de xadrez experimental que utiliza Data Mining e Motores de IA para simular o estilo de jogo de usuários reais do Chess.com. O projeto integra uma interface moderna com um backend robusto em Python, permitindo que jogadores treinem contra "clones" digitais baseados em históricos de partidas.

## 🧠 A Lógica da Engine

A engine não apenas busca o melhor lance, mas tenta mimetizar o comportamento do jogador alvo:

**Extração de DNA:** O sistema consome a API do Chess.com para identificar padrões de abertura e frequência de vitórias.

**Mimetismo Técnico:** Utiliza o motor Stockfish para validar lances, ajustando a "agressividade" e o nível de erro conforme o perfil identificado.

**Interface Tática:** Desenvolvido com foco em usabilidade, permitindo análise em tempo real e visualização PGN.

**🛠️ Tecnologias Utilizadas Backend:** Python 3.12, Flask.

**Engine de Xadrez:** Stockfish 16.1.

**Frontend:** HTML5, CSS3 (Flexbox/Grid), Chessboard.js, Chess.js.

**Infraestrutura:** Docker & Gunicorn.

🚀 Como Executar o Projeto (Localmente)
Você pode rodar o projeto de forma isolada e segura utilizando o Docker.

## Pré-requisitos
Docker instalado (testado no Linux Mint).

## Passo a Passo

1. **Clonar o repositório:**

```bash
git clone https://github.com/PhaellZX/mimesis_engine.git
cd mimesis-avalanche
```

2. **Construir a imagem Docker:**

Este comando instala todas as dependências, incluindo o Python, as bibliotecas de xadrez e o motor Stockfish dentro de um container.

```bash
docker build -t mimesis-app .
```

3.  **Executar o container:**
    O projeto estará disponível na porta 5000 do seu navegador.
    
```bash
    docker run -p 5000:5000 mimesis-app
```

4.  **Acessar a aplicação:**
    Abra o navegador e acesse: `http://localhost:5000`

---

## 📈 Roadmap & Evolução
- [x] Integração com API Chess.com.
- [x] Dockerização do ambiente de execução.
- [ ] Implementação de Redes Neurais para predição de lances específicos do usuário.
- [ ] Interface mobile-friendly.

## ✒️ Autor
**Raphael** – Especialista em Tecnologia em Analista e Desenvolvimento de Sistemas.

