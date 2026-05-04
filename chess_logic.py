import requests
import chess.pgn
import io

def get_player_games(username, year, month):
    # Formato do mês deve ser '01', '02', etc.
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
    headers = {"User-Agent": "SeuNomeApp - contato: seu@email.com"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    
    games = response.json().get('games', [])
    return games

def analyze_style(games, username):
    stats = {"vitorias": 0, "derrotas": 0, "aberturas": {}}
    
    for game in games:
        # Analisando o PGN para extrair a abertura
        pgn_text = game.get('pgn')
        if not pgn_text: continue
        
        pgn = io.StringIO(pgn_text)
        game_obj = chess.pgn.read_game(pgn)
        
        # Pega a abertura (Header ECO ou Opening)
        opening = game_obj.headers.get("Opening", "Desconhecida")
        stats["aberturas"][opening] = stats["aberturas"].get(opening, 0) + 1
        
        # Verifica resultado
        white = game_obj.headers.get("White").lower()
        result = game_obj.headers.get("Result")
        
        if (white == username.lower() and result == "1-0") or \
           (white != username.lower() and result == "0-1"):
            stats["vitorias"] += 1
        else:
            stats["derrotas"] += 1
            
    return stats

def build_move_probabilities(games, username):
    move_map = {}
    count_moves = 0 # Para debug

    for game in games:
        pgn_text = game.get('pgn')
        if not pgn_text: continue
        
        pgn = io.StringIO(pgn_text)
        game_obj = chess.pgn.read_game(pgn)
        board = game_obj.board()
        
        # Normaliza o nome para comparação
        white_player = game_obj.headers.get("White", "").lower()
        target_color = chess.WHITE if white_player == username.lower() else chess.BLACK
        
        for move in game_obj.mainline_moves():
            fen = board.fen().split(' ')[0]
            
            if board.turn == target_color:
                if fen not in move_map:
                    move_map[fen] = {}
                move_str = move.uci()
                move_map[fen][move_str] = move_map[fen].get(move_str, 0) + 1
                count_moves += 1
            
            board.push(move)
    
    print(f"Modelo criado para {username} com {count_moves} lances mapeados.")
    return move_map