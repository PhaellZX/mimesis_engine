# 🪄 Mimesis Engine | Chess Intelligence Engine

Mimesis Engine is an experimental chess platform that uses data mining and AI engines to simulate the playing styles of real Chess.com users. The project integrates a modern interface with a robust Python backend, allowing players to train against digital "clones" based on match histories.

## 🧠 The Engine Logic

The engine not only seeks the best move but also attempts to mimic the target player's behavior:

**DNA Extraction:** The system consumes the Chess.com API to identify opening patterns and win frequencies.

**Technical Mimicry:** Uses the Stockfish engine to validate moves, adjusting "aggressiveness" and error levels according to the identified profile.

**Tactical Interface:** Developed with a focus on usability, enabling real-time analysis and PGN visualization.

**🛠️ Backend Technologies Used:** Python 3.12, Flask.

**Chess Engine:** Stockfish 16.1.

**Frontend:** HTML5, CSS3 (Flexbox/Grid), Chessboard.js, Chess.js.

**Infrastructure:** Docker & Gunicorn.

🚀 How to Run the Project (Locally)
You can run the project in an isolated and secure manner using Docker.

## Prerequisites
Docker installed (tested on Linux Mint).

## Step-by-Step

1. **Clone the repository:**

```bash
git clone https://github.com/PhaellZX/mimesis_engine.git
cd mimesis-avalanche
```

2. **Build the Docker image:**

This command installs all dependencies—including Python, chess libraries, and the Stockfish engine—inside a container.

```bash
docker build -t mimesis-app .
```

3.  **Run the container:**

The project will be available on port 5000 in your browser.
    
```bash
    docker run -p 5000:5000 mimesis-app
```

4.  **Access the application:**
Open your browser and go to: `http://localhost:5000`

---

## 📈 Roadmap & Evolution
- [x] Integration with the Chess.com API.
- [x] Dockerization of the runtime environment.
- [ ] Implementation of Neural Networks to predict user-specific moves.
- [ ] Mobile-friendly interface.

## ✒️ Author
**Raphael** – Specialist in Systems Analysis and Development.
