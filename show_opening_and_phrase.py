import json
from collections import defaultdict

# Charger les données
with open("top_opening_white.json", "r") as f:
    data = json.load(f)
    
    
    
import chess

def get_fen_from_plays(plays):
    """
    Convertit une séquence de coups en notation UCI en position FEN.
    :param plays: Une chaîne de coups séparés par des virgules (notation UCI).
    :return: La position FEN résultante après avoir appliqué les coups.
    """
    # Créer un échiquier standard
    board = chess.Board()
    
    # Appliquer chaque coup
    for move in plays.split(","):
        try:
            board.push_uci(move)  # Applique le coup en UCI
        except ValueError:
            print(f"Le coup '{move}' est invalide.")
            return None
    
    # Retourne la position FEN après les coups
    return board.fen()

# Grouper les données par 'name'
openings = defaultdict(list)
for entry in data:
    opening_name = entry["name"]["name"]
    openings[opening_name].append(entry)

def find_common_prefix(texts, separator=' '):
    """
    Trouve le préfixe commun parmi plusieurs chaînes.
    """
    if not texts:
        return ""
    
    # Découper chaque texte en une liste de mots
    split_texts = [text.split(separator) for text in texts]
    
    # Trouver le préfixe commun
    common_prefix = []
    for words in zip(*split_texts):
        if all(word == words[0] for word in words):
            common_prefix.append(words[0])
        else:
            break
    
    return " ".join(common_prefix)

commun_fens = []
# Parcourir les groupes pour trouver le tronçon commun
for name, lines in openings.items():
    texts = [line["plays"] for line in lines]
    common_prefix_play = find_common_prefix(texts, ',')
    common_prefix_text = find_common_prefix([line["text"] for line in lines])
    fen = get_fen_from_plays(','.join(common_prefix_play.split(' ')))
    print(f"\n--- Nouvelle ouverture : {name} ---")
    for line in lines:
        print(f"({line['count']:>2}) cp:{line['cp']:>3}) {line['text']}")
    print(f"FEN: {fen}")
    if fen not in commun_fens:
      commun_fens.append(fen)
    print(f"text commun: {common_prefix_text}")
    
    
print(f"commun to known {len(commun_fens)}")