import os
import sqlite3
import random
import chess
import chess.engine
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from chess_logic import get_player_games, analyze_style, build_move_probabilities

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
DB_NAME = "chess_data.db"
# Caminho absoluto ou relativo para o binário do Stockfish
STOCKFISH_PATH = os.environ.get('STOCKFISH_PATH', './engine/stockfish/stockfish-ubuntu-x86-64-avx2') 

# Memória para evitar repetição infinita na partida atual
game_history = []

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS player_models (
                username TEXT,
                fen TEXT,
                move_uci TEXT,
                frequency INTEGER,
                PRIMARY KEY (username, fen, move_uci)
            )
        """)
init_db()

def save_model_to_db(username, move_map):
    with sqlite3.connect(DB_NAME) as conn:
        for fen, moves in move_map.items():
            for move, freq in moves.items():
                conn.execute("""
                    INSERT OR REPLACE INTO player_models (username, fen, move_uci, frequency)
                    VALUES (?, ?, ?, ?)
                """, (username.lower(), fen, move, freq))

def get_historical_moves(username, fen):
    fen_key = fen.split(' ')[0]
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("""
            SELECT move_uci FROM player_models 
            WHERE username = ? AND fen = ? 
            ORDER BY frequency DESC
        """, (username.lower(), fen_key))
        return [row[0] for row in cursor.fetchall()]

@app.route('/', methods=['GET', 'POST'])
def index():
    global game_history
    analysis = None
    username = None
    user_color = 'white'
    
    if request.method == 'POST':
        game_history = [] # Reinicia histórico em nova análise
        username = request.form.get('username')
        user_color = request.form.get('user_color')
        
        all_games = []
        winning_games = []
        now = datetime.now()
        current_year, current_month = now.year, now.month

        # Varredura de 6 meses para coletar o DNA do jogador
        for i in range(6):
            month = current_month - i
            year = current_year
            if month <= 0:
                month += 12
                year -= 1
            
            month_games = get_player_games(username, year, f"{month:02d}")
            if month_games:
                all_games.extend(month_games)
                for g in month_games:
                    # Filtro de vitórias para maior qualidade técnica
                    w_user = g.get('white', {}).get('username', '').lower()
                    b_user = g.get('black', {}).get('username', '').lower()
                    if (w_user == username.lower() and g['white']['result'] == 'win') or \
                       (b_user == username.lower() and g['black']['result'] == 'win'):
                        winning_games.append(g)

        if all_games:
            analysis = analyze_style(all_games, username)
            source = winning_games if winning_games else all_games
            move_map = build_move_probabilities(source, username)
            save_model_to_db(username, move_map)
            
    return render_template('index.html', analysis=analysis, username=username, user_color=user_color, level=request.form.get('level'))

@app.route('/get_move', methods=['POST'])
def get_move():
    global game_history
    fen = request.form.get('fen')
    username = request.form.get('username')
    difficulty = request.form.get('level', 'normal') # easy, normal, hard, legend
    
    if not fen or not username:
        return jsonify({"move": None})

    board = chess.Board(fen)
    if board.fullmove_number <= 1:
        game_history = []

    # Configuração de Margem de Erro (Centipawns) e Nível de Habilidade
    levels = {
        'easy':   {'margin': -400, 'skill': 2,  'time': 0.05},
        'normal': {'margin': -200, 'skill': 8,  'time': 0.1},
        'hard':   {'margin': -100, 'skill': 15, 'time': 0.15},
        'legend': {'margin': -50,  'skill': 20, 'time': 0.2}
    }
    conf = levels.get(difficulty, levels['normal'])
    selected_move = None

    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        engine.configure({"Skill Level": conf['skill']})
        
        # 1. Tenta encontrar um lance no DNA histórico que passe no crivo do nível
        historical_moves = get_historical_moves(username, fen)
        
        for move_uci in historical_moves:
            try:
                move_obj = chess.Move.from_uci(move_uci)
                if move_obj in board.legal_moves:
                    # Validação tática
                    info = engine.analyse(board, chess.engine.Limit(time=conf['time']), root_moves=[move_obj])
                    score_obj = info.get("score") if isinstance(info, dict) else info[0].get("score")
                    
                    if score_obj:
                        val = score_obj.relative.score()
                        # Aceita se estiver dentro da margem de erro do nível escolhido
                        if score_obj.relative.is_mate() or (val is not None and val > conf['margin']):
                            if move_uci not in game_history[-4:]:
                                selected_move = move_uci
                                break
            except:
                continue

        # 2. Fallback: Se não houver histórico aceitável, a engine assume o controle
        if not selected_move:
            result = engine.play(board, chess.engine.Limit(time=conf['time']))
            selected_move = result.move.uci()

        engine.quit()

    except Exception as e:
        print(f"Erro na Engine: {e}")
        return jsonify({"error": str(e)}), 500

    if selected_move:
        game_history.append(selected_move)

    return jsonify({"move": selected_move})

if __name__ == '__main__':
    app.run(debug=True)