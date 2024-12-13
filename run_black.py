import requests
import chess
import pprint
import random
import os
from time import sleep
import json


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
            "total_games": total,
            "freq": round(freq_move, 2),
            "white": round(winrate_white, 2),
            "black": round(winrate_black, 2),
            "draws": round(draw_rate, 2),
            "uci": move["uci"],
            "averageRating": move["averageRating"]
        }
        opening["moves"].append(line)

    return opening

def get_openings(play: str, rating: str, move: int = 12, retries: int = 3, filename=None):
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
  
  url = "https://explorer.lichess.ovh/lichess"
  params = {
      "play": play,
      "ratings": rating,
      "moves": move
  }

  for attempt in range(retries):
    try:
      response = requests.get(url, params=params)
      status_code = response.status_code
      response.raise_for_status()  # Vérifie les erreurs HTTP
      result = extract_data(response.json())
      
      opening_cache[play] = result
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

def get_top_computer_move(start_opening, count, color: str, fen: str, moves, filename='data/computer.json'):
  if os.path.exists(filename):
    with open(filename, 'r') as f:
        fen_cache = json.load(f)
  else:
    fen_cache = {}

  if fen in fen_cache:
    cp = fen_cache[fen]['cp']
    top_move = fen_cache[fen]['top_move']
    print(f"({start_opening}) {count:<3} --> computer='{top_move}' cp={cp}")
    return top_move

  try:
    response = requests.get(
        "https://lichess.org/api/cloud-eval",
        params={
            "fen": fen,
            "multiPv": 50,
        }
    )
    data = response.json()
    if color == 'black':
      better = min(data['pvs'], key=lambda x: x['cp'])
    elif color == 'white':
      better = max(data['pvs'], key=lambda x: x['cp'])
    else:
      raise ValueError("La couleur doit être 'white' ou 'black'.")

    top_move = better['moves'].split(' ')[0]
    better['moves'] = moves
    better['top_move'] = top_move
    fen_cache[fen] = better  # Stocker le FEN et le coup dans le cache

    # Enregistrer le cache mis à jour dans le fichier JSON
    with open(filename, 'w') as f:
      json.dump(fen_cache, f, separators=(',', ': '), indent=4)
    print(f"({start_opening}) {count:<3} --> computer='{top_move}' cp={better['cp']}")
    return top_move

  except Exception as e:
    print(f"Erreur lors de l'appel API : {e}")
    raise Exception("error")
  
  
openings = []



############################ TOP ENTRY ##################################################
COMPUTER_COLOR = 'black'
START_OPENINGS = {
  'e2e4': 0,
  'd2d4': 0,
  'g1f3': 0,
  'c2c4': 0,
  'e2e3': 250,
  'g2g3': 250,
  'b2b3': 250
}
for start_opening, count in START_OPENINGS.items():
  board = chess.Board()
  board.push(chess.Move.from_uci(start_opening))
  START_FEN = board.fen()
  FILENAME_COMPUTER = f'data/computer_{COMPUTER_COLOR}/computer.json'
  FILENAME_PLAYER = f'data/computer_{COMPUTER_COLOR}/random_play_{start_opening}.json'

  for i in range(count):
    board = chess.Board()
    board.set_fen(START_FEN)
    moves = [start_opening]
    while True:
      try:
        if COMPUTER_COLOR == 'white' and len(moves) % 2 == 0:
          new_fen = board.fen()
          top_move = get_top_computer_move(start_opening, i, color=computer_color, fen=new_fen, moves=moves)
          moves.append(top_move)
          board.push(chess.Move.from_uci(top_move))
          
        if COMPUTER_COLOR == 'white' and len(moves) % 2 == 1:
          play = ','.join(map(str, moves))
          opening = get_openings(play=play, rating="0,3000", move=20)
          result = choice_a_play(openings={play: opening}, play=play)
          moves.append(result['uci2'])
          board.push(chess.Move.from_uci(result['uci2']))
          print(f"({start_opening}) {i:<3} --> random_p='{result['uci2']}' freq={result['freq']}% winrate={result['black']}")
          
        if COMPUTER_COLOR == 'black' and len(moves) % 2 == 1:
          new_fen = board.fen()
          top_move = get_top_computer_move(start_opening, i, color=COMPUTER_COLOR, fen=new_fen, moves=moves, filename=FILENAME_COMPUTER)
          moves.append(top_move)
          board.push(chess.Move.from_uci(top_move))
          
        if COMPUTER_COLOR == 'black' and len(moves) % 2 == 0:
          play = ','.join(map(str, moves))
          opening = get_openings(play=play, rating="0,3000", move=20, filename=FILENAME_PLAYER)
          result = choice_a_play(openings={play: opening}, play=play)
          moves.append(result['uci2'])
          board.push(chess.Move.from_uci(result['uci2']))
          print(f"({start_opening}) {i:<3} --> random_p='{result['uci2']}' freq={result['freq']}% winrate={result['black']}")
          
          
      except Exception as e:
        print(f"------------finish opening------------")
        print(' '.join(map(str, moves)))
        print(board.fen())
        print('---------------------------------------')
        break
      
    