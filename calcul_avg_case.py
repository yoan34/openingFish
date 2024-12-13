
import json
import chess


result = {}
result2 = {}
for filename in ['c2c4','d2d4','e2e3','e2e4','g1f3']:
    with open(f'data/computer_black/random_play_{filename}.json', 'r') as f:
        data = json.load(f)
        
    print(f"START {filename}")
    for opening in data:
      board = chess.Board()
      move_list = opening.split(',')
      for move in move_list:
        chess_move = board.push_san(move)
        destination_square = chess_move.to_square
        piece = board.piece_at(destination_square)
        key = f"{move[2:4]}_{piece.symbol().lower()}"
        if move[2:4] not in result2:
          result2[move[2:4]] = 0
        result2[move[2:4]] += 1
        if key not in result:
          result[key] = 0
        result[key] += 1
        
        
with open(f'data/computer_white/random_play.json', 'r') as f:
    data = json.load(f)
    
for opening in data:
  board = chess.Board()
  move_list = opening.split(',')
  for move in move_list:
    chess_move = board.push_san(move)
    destination_square = chess_move.to_square
    piece = board.piece_at(destination_square)
    key = f"{move[2:4]}_{piece.symbol().lower()}"
    if move[2:4] not in result2:
      result2[move[2:4]] = 0
    result2[move[2:4]] += 1
    if key not in result:
      result[key] = 0
    result[key] += 1


from pprint import pprint

sorted_data = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

  
  
print(len(sorted_data))


sorted_data2 = dict(sorted(result2.items(), key=lambda item: item[1], reverse=True))
sorted_data3 = dict(sorted(result2.items()))

for k,v in sorted_data3.items():
  print(f"{k} --> {v}")
s = ''
for k,v in sorted_data3.items():

  if '8' in k:
    s+= f'{v:<7}\n'
  else:
    s += f"{v:<7}"
    
  
print(s)
  
print(len(sorted_data3))