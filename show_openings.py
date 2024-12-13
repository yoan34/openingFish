import json
import chess


with open('data/computer_black/random_play_d2d4.json', 'r') as f:
    data = json.load(f)
    
with open('data/computer_black/computer.json', 'r') as f:
    fens = json.load(f)
    
    
def calculate_prob_of_opening(moves):
    start_prob = {
        "e2e3": 0.02,
        "d2d4": 0.25
    }
    moves = moves.split(',')
    total_prob = start_prob[moves[0]]
    for i in range(0, len(moves)-1, 2):
        the_play = moves[i]
        key = ','.join(moves[:i])
        if key:
            opening = data[key]
            move = next((move for move in opening['moves'] if move["uci"] == the_play), None)
            total_prob *= (move['freq']/100)
    return total_prob*100
        

# Charger les données depuis le fichier JSON


# Trier les lignes d'ouverture par ordre alphabétique pour regrouper les lignes similaires
sorted_openings = sorted(data.items())

# Liste pour stocker la plus longue version de chaque ouverture avec ses données
unique_openings = []

previous_opening = ""
for opening, details in sorted_openings:
    # Garder l'ouverture si elle est plus longue et commence par la même séquence que la précédente
    if not previous_opening or not opening.startswith(previous_opening):
        unique_openings.append((opening, details))
        previous_opening = opening
    elif opening.startswith(previous_opening) and len(opening) > len(previous_opening):
        # Remplace l'ouverture précédente par la plus longue
        unique_openings[-1] = (opening, details)
        previous_opening = opening


total_cp = 0
total_count = 0
cps = []
per_prob = {}
for opening, details in unique_openings:
    board = chess.Board()
    for move_uci in opening.split(',')[:-1]:
        board.push_uci(move_uci)
    fen=board.fen()
    fen_data = fens[fen]
    cp = fen_data['cp']
    if cp < 2000:
        total_cp+= cp
        total_count += 1
        cps.append(cp)
    name = details.get('name').get('name', 'unknown')
    per_prob[opening] = calculate_prob_of_opening(opening)
    print(f"{name:<80} {opening} cp={cp}")
    
print(f"avg cp {(total_cp/total_count):.2f}")
cps.sort()
print(cps)

sorted_data = dict(sorted(per_prob.items(), key=lambda item: item[1], reverse=True))
RESULT = {}
for k, v in sorted_data.items():
    L = len(k.split(','))
    if L not in RESULT:
        RESULT[L] = []
    RESULT[L].append({k: v})
    # print(f"{k:<80} {v:.10f}")
    
from pprint import pprint

# print(RESULT.keys())

# for i in range(4,30,2):
#     pprint(RESULT[i])

moves = "d2d4,g8f6,c2c4,g7g6,f2f3,f8g7,e2e4,e8h8,c1e3,d7d6,g1e2,b8d7,b1c3".split(',')
board = chess.Board()

# Appliquer chaque coup et afficher l'état du plateau
for move in moves:
    # Convertir le mouvement en format UCI (par ex. "d2d4" devient un objet Move)
    chess_move = chess.Move.from_uci(move)
    # Appliquer le mouvement
    board.push(chess_move)
    
    # Récupérer la case de destination du mouvement
    destination_square = chess_move.to_square
    # Récupérer la pièce qui se trouve maintenant sur la case de destination
    piece = board.piece_at(destination_square)
    
    # Afficher le résultat
    # print(f"Après le coup {move}, la case {chess.square_name(destination_square)} contient : {piece.symbol() if piece else 'Aucune pièce'}")
    # print("---------------")
    
    
# if __name__ == "__main__":
#     play = 'e2e3,g8f6,g1f3,d7d5,d2d3,c7c5,f1e2,g7g6,e1h1,b8c6'
#     play = "e2e3,g8f6,g1f3,d7d5,b1c3,e7e6,d2d3,c7c5,f1e2,b8c6,e1h1,e6e5,d3d4,e5e4"
#     play = 'e2e3,g8f6,d2d4,d7d5,c2c4,e7e6,b1c3,b7b6,g1f3,f8d6,a2a3,e8h8,f1d3,d5c4'
#     print(f"{play=}")
#     calculate_prob_of_opening(play)
    