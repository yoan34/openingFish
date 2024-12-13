import requests
import chess
import pprint
import random
import os
from time import sleep
import json


token = "lip_McRjLYyLVpkRdC3hOfru"

def choice_a_play(openings: dict, play: str):
    moves_data = openings[play].get("moves", [])
    moves = [move["uci"] for move in moves_data]
    weights = [move["freq"] for move in moves_data]
    if not moves or not weights:
        return {"error": "no more line"}

    selected_move = random.choices(moves, weights=weights, k=1)[0]
    selected_move_uci = random.choices(moves, weights=weights, k=1)[0]
    selected_move = next(move for move in moves_data if move["uci"] == selected_move_uci)
    move = f"{selected_move_uci[:2]}-{selected_move_uci[2:]}"
    selected_move["uci"] = move
    selected_move["uci2"] = selected_move_uci
    selected_move["name"] = openings[play]["name"]
    return selected_move

def extract_data(data):
    opening = {"moves": [], "count": 0}
    total_games = sum(sum([move["white"], move["black"], move["draws"]]) for move in data["moves"])

    opening["total_game_move"] = total_games
    opening["name"] = data.get("opening", None)

    for move in data["moves"]:
        total = move["black"] + move["white"] + move["draws"]
        winrate_white = move["white"] / total * 100
        winrate_black = move["black"] / total * 100
        draw_rate = move["draws"] / total * 100
        freq_move = total / total_games * 100
        line = {
            "freq": round(freq_move, 2),
            "uci": move["uci"],
        }
        opening["moves"].append(line)

    return opening

def get_openings(play: str, fen:str, cp: int, rating: str, move: int = 12, retries: int = 3, filename=None):
  if os.path.exists(filename):
    with open(filename, 'r') as f:
        opening_cache = json.load(f)
  else:
    opening_cache = {}

  if play in opening_cache:
    print(f"opening already exist")
    opening_cache[play]['count'] += 1
    with open(filename, 'w') as f:
      json.dump(opening_cache, f, indent=4)
    
    return opening_cache[play]
  
  headers = {"Authorization": f"Bearer {token}"}
  url = "https://explorer.lichess.ovh/lichess"
  params = {
      "play": play,
      "ratings": rating,
      "moves": move
  }

  for attempt in range(retries):
    try:
      response = requests.get(url, params=params, headers=headers)
      status_code = response.status_code
      response.raise_for_status()  # Vérifie les erreurs HTTP
      result = extract_data(response.json())
      
      opening_cache[play] = result
      opening_cache[play]['fen'] = fen
      opening_cache[play]['cp'] = cp
      with open(filename, 'w') as f:
        json.dump(opening_cache, f, indent=4)
      return result
    
    except requests.exceptions.HTTPError as http_err:
      print(f"HTTP error occurred: code={status_code} {http_err} - Attempt {attempt + 1} of {retries}")
      print(f"MOVE NOT CORRECT PROBABILITY")

    except requests.exceptions.ConnectionError as conn_err:
      print(f"Connection error occurred: code={status_code}{conn_err} - Attempt {attempt + 1} of {retries}")

    except requests.exceptions.Timeout as timeout_err:
      print(f"Timeout error occurred: code={status_code}{timeout_err} - Attempt {attempt + 1} of {retries}")

    except requests.exceptions.RequestException as req_err:
      print(f"Error during GET openings: code={status_code}{req_err} - Attempt {attempt + 1} of {retries}")

    except ValueError as val_err:
      print(f"JSON decoding failed: code={status_code}{val_err} - Attempt {attempt + 1} of {retries}")


    if attempt < retries - 1:  # Attendre seulement si ce n'est pas le dernier essai
      print("Waiting 60s before retrying...")
      sleep(60)
  print(f"Failed to get data after {retries} attempts.")
  raise Exception("error")

def get_top_computer_move(start_opening, count, color: str, fen: str, moves, filename='data/computer.json', retries=3):
    # Charger le cache
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            fen_cache = json.load(f)
    else:
        fen_cache = {}

    # Vérifier si le FEN est déjà dans le cache
    if fen in fen_cache:
        cp = fen_cache[fen]['cp']
        top_move = fen_cache[fen]['top_move']
        print(f"({start_opening}) {count:<3} --> computer='{top_move}' cp={cp}")
        return top_move, cp

    # Paramètres de la requête
    url = "https://lichess.org/api/cloud-eval"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"fen": fen, "multiPv": 50}

    # Effectuer les tentatives avec retries
    for attempt in range(retries):
        try:
            print(f"before cloud_eval - Attempt {attempt + 1}/{retries}")
            response = requests.get(url, params=params, headers=headers)
            status_code = response.status_code
            response.raise_for_status()  # Lève une exception pour les erreurs HTTP
            print(f"after cloud_eval - Status Code: {status_code}")

            # Analyser la réponse JSON
            data = response.json()
            if color == 'black':
                better = min(data['pvs'], key=lambda x: x['cp'])
            elif color == 'white':
                better = max(data['pvs'], key=lambda x: x['cp'])
            else:
                raise ValueError("La couleur doit être 'white' ou 'black'.")

            # Mettre à jour le cache
            top_move = better['moves'].split(' ')[0]
            better['moves'] = moves
            better['top_move'] = top_move
            fen_cache[fen] = better

            with open(filename, 'w') as f:
                json.dump(fen_cache, f, indent=4)

            print(f"({start_opening}) {count:<3} --> computer='{top_move}' cp={better['cp']}")
            return top_move, better['cp']

        except requests.exceptions.HTTPError as http_err:
          if (status_code == 404):
            raise ValueError("end of opening}")
            print(f"HTTP error occurred: {http_err} - Attempt {attempt + 1} of {retries}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err} - Attempt {attempt + 1} of {retries}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err} - Attempt {attempt + 1} of {retries}")
        except requests.exceptions.RequestException as req_err:
            print(f"General error occurred: {req_err} - Attempt {attempt + 1} of {retries}")
        except ValueError as val_err:
            print(f"JSON decoding failed: {val_err} - Attempt {attempt + 1} of {retries}")

        # Attendre avant de réessayer, sauf après la dernière tentative
        if attempt < retries - 1:
            print("Waiting 60s before retrying...")
            sleep(60)

    # Si toutes les tentatives échouent, lever une exception
    print(f"Failed to get data after {retries} attempts.")
    raise Exception("Failed to get top computer move after retries.")
  
def get_next_fen(fen: str, move: str) -> str:
  board = chess.Board(fen)
  chess_move = chess.Move.from_uci(move)
  if chess_move in board.legal_moves:
      board.push(chess_move)
      return board.fen()
  else:
      raise ValueError(f"Mouvement illégal: {move}")

def get_opening_name(play: str, rating: str, fen: str,  move: int = 2, retries: int = 3, filename='data/opening_name.json'):
  if os.path.exists(filename):
    with open(filename, 'r') as f:
        opening_cache = json.load(f)
  else:
    opening_cache = {}

  if play in opening_cache:
    print(f"opening name already exist")
    return opening_cache[play]
  
  url = "https://explorer.lichess.ovh/lichess"
  params = {
      "play": play,
      "ratings": rating,
      "moves": move,
  }

  for attempt in range(retries):
    try:
      response = requests.get(url, params=params)
      status_code = response.status_code
      response.raise_for_status()  # Vérifie les erreurs HTTP
      result = extract_data(response.json())
      
      opening_cache[play] = result['name']
      opening_cache[play]['fen'] = fen
      with open(filename, 'w') as f:
        json.dump(opening_cache, f, indent=4)
      return opening_cache[play]
    
    except requests.exceptions.HTTPError as http_err:
      print(f"HTTP error occurred: code={status_code} {http_err} - Attempt {attempt + 1} of {retries}")
      print(f"MOVE NOT CORRECT PROBABILITY")

    except requests.exceptions.ConnectionError as conn_err:
      print(f"Connection error occurred: code={status_code}{conn_err} - Attempt {attempt + 1} of {retries}")

    except requests.exceptions.Timeout as timeout_err:
      print(f"Timeout error occurred: code={status_code}{timeout_err} - Attempt {attempt + 1} of {retries}")

    except requests.exceptions.RequestException as req_err:
      print(f"Error during GET openings: code={status_code}{req_err} - Attempt {attempt + 1} of {retries}")

    except ValueError as val_err:
      print(f"JSON decoding failed: code={status_code}{val_err} - Attempt {attempt + 1} of {retries}")


    if attempt < retries - 1:  # Attendre seulement si ce n'est pas le dernier essai
      print("Waiting 60s before retrying...")
      sleep(60)
  print(f"Failed to get data after {retries} attempts.")
  raise Exception("error")
openings = []

############################ TOP ENTRY ##################################################
COMPUTER_COLOR = 'white'

board = chess.Board()
start_opening = 'd2d4'
board.push(chess.Move.from_uci(start_opening))
START_FEN = board.fen()
FILENAME_COMPUTER = f'data/computer_{COMPUTER_COLOR}/computer.json'
FILENAME_PLAYER = f'data/computer_{COMPUTER_COLOR}/random_play.json'

for i in range(200):
  board = chess.Board()
  board.set_fen(START_FEN)
  moves = [start_opening]
  cp = None
  while True:
    try:
      
      if COMPUTER_COLOR == 'white' and len(moves) % 2 == 0:
        new_fen = board.fen()
        top_move, cp = get_top_computer_move(start_opening, i, color=COMPUTER_COLOR, fen=new_fen, moves=moves, filename=FILENAME_COMPUTER)

        moves.append(top_move)
        board.push(chess.Move.from_uci(top_move))
        
      if COMPUTER_COLOR == 'white' and len(moves) % 2 == 1:
        play = ','.join(map(str, moves))
        opening = get_openings(play=play, fen=board.fen(), cp=cp, rating="0,1800", move=10, filename=FILENAME_PLAYER)
        result = choice_a_play(openings={play: opening}, play=play)

        moves.append(result['uci2'])
        board.push(chess.Move.from_uci(result['uci2']))
        print(f"({start_opening}) {i:<3} --> random_p='{result['uci2']}' freq={result['freq']}%")
        
      if len(moves) >= 15:
        print("Opening finish because 13 moves plays")
        raise ValueError("Opening finish because 13 moves plays")
        
      

        
    except Exception as e:
      print(f"------------finish opening------------")
      print(' '.join(map(str, moves)))
      print(board.fen())
      print('---------------------------------------')
      break
      
    