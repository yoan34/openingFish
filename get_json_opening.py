"""
Je dois créer un format de donnée pour pouvoir l'afficher en html et l'imprimer:
Je veux une structure avec:
- FEN
- moves e2e4,e7e5...
- cp  OK
- freq  --> j'ai un count pour chaque ouverture
-name  --> j'ai le name
- phrase goku...

Je dois les récupérer par ordre alphabétique  en récupérant les TOP 100 probas par exemple
{1: 1, 3: 10, 5: 56, 7: 145, 9: 244, 11: 315}
{1: 1, 3: 10, 5: 85, 7: 325, 9: 681, 11: 1047}
{1: 1, 3: 10, 5: 72, 7: 245, 9: 471, 11: 653, 13: 799, 15: 841}
"""

import json



def get_phrase(plays):
  s = ''
  moves = plays.split(',')
  for i, move in enumerate(moves):
    if  i % 2 == 0:
      s += f" {white_system[move[2:4]]}"
    else:
      s += f" {black_system[move[2:4]]}"
  return s.strip()
# récupérer toutes les ouvertures
white_system = {
  'a8': 'citadelle', 'b8': 'tarzan', 'c8': 'gandalf', 'd8': 'tintin', 'e8': 'césar', 'f8': 'frankenstein', 'g8': 'roméo', 'h8': 'temple',
  'a7': 'michael', 'b7': 'dague', 'c7': 'hercule', 'd7': 'dracula', 'e7': 'spiderman', 'f7': 'dragon', 'g7': 'pistolet', 'h7': 'astérix',
  'a6': 'garfield', 'b6': 'hache', 'c6': 'bambi', 'd6': 'obélix', 'e6': 'aquaman', 'f6': 'batman', 'g6': 'bombe', 'h6': 'trump',
  'a5': 'caverne', 'b5': 'einstein', 'c5': 'jungle', 'd5': 'napoléon', 'e5': 'jésus', 'f5': 'désert', 'g5': 'mozart', 'h5': 'lune',
  'a4': 'grotte', 'b4': 'voltaire', 'c4': 'chateau', 'd4': 'goku', 'e4': 'simba', 'f4': 'montagne', 'g4': 'pythagore', 'h4': 'mars',
  'a3': 'cléopatre', 'b3': 'arc', 'c3': 'léonidas', 'd3': 'thanos', 'e3': 'merlin', 'f3': 'lancelot', 'g3': 'couteau', 'h3': 'minotaure',
  'a2': 'lilith', 'b2': 'épée', 'c2': 'ironman', 'd2': 'deadpool', 'e2': 'wolverine', 'f2': 'thor', 'g2': 'marteau', 'h2': 'hadès',
  'a1': 'taverne', 'b1': 'zorro', 'c1': 'ulysse', 'd1': 'achille', 'e1': 'moïse', 'f1': 'alladin', 'g1': 'yoda', 'h1': 'donjon',
}

black_system = {
  'a8': 'résister', 'b8': 'balancer', 'c8': 'préserver', 'd8': 'explorer', 'e8': 'gouverner', 'f8': 'fabriquer', 'g8': 'aimer', 'h8': 'vénérer',
  'a7': 'danser', 'b7': 'poignarder', 'c7': 'soulever', 'd7': 'mordre', 'e7': 'grimper', 'f7': 'garder', 'g7': 'tirer', 'h7': 'courageux',
  'a6': 'manger', 'b6': 'fendre', 'c6': 'bondir', 'd6': 'porter', 'e6': 'nager', 'f6': 'traquer', 'g6': 'exploser', 'h6': 'président',
  'a5': 'explorer', 'b5': 'réfléchir', 'c5': 'cacher', 'd5': 'conquérir', 'e5': 'prier', 'f5': 'seul', 'g5': 'composer', 'h5': 'planner',
  'a4': 'hiberner', 'b4': 'critiquer', 'c4': 'fort', 'd4': 'voler', 'e4': 'rugir', 'f4': 'escalader', 'g4': 'calculer', 'h4': 'voyager',
  'a3': 'reigner', 'b3': 'viser', 'c3': 'défendre', 'd3': 'anéantir', 'e3': 'enchanter', 'f3': 'chevaucher', 'g3': 'jeter', 'h3': 'gardien',
  'a2': 'ténébreux', 'b2': 'couper', 'c2': 'inventer', 'd2': 'rire', 'e2': 'trancher', 'f2': 'éclair', 'g2': 'frapper', 'h2': 'méchant',
  'a1': 'fêter', 'b1': 'signer', 'c1': 'ruser', 'd1': 'combattre', 'e1': 'séparer', 'f1': 'souhaiter', 'g1': 'enseigner', 'h1': 'enfermer',
}

with open("data/computer_white/random_play.json", "r") as f:
  openings = json.load(f)
  
  
  
OPENINGS = []
OPENINGS_5 = []
OPENINGS_4 = []
OPENINGS_BY_MOVE = {}
for opening, values in openings.items():
  item = values
  item['plays'] = opening
  item['text'] = get_phrase(opening)
  if len(opening.split(',')) not in OPENINGS_BY_MOVE:
    OPENINGS_BY_MOVE[len(opening.split(','))] = 0
  OPENINGS_BY_MOVE[len(opening.split(','))] += 1
  if len(opening.split(',')) == 11:
    OPENINGS_5.append(item)
  if len(opening.split(',')) == 13:
    OPENINGS_4.append(item)
    OPENINGS.append(item)
  
  
  
top_count_openings = sorted(OPENINGS, key=lambda x: x['count'], reverse=True)[:200]
  

top_count_openings = sorted(
    top_count_openings,
    key=lambda x: (x['name']['name'], -x['count'])
)
  
  
with open("top_opening_white.json", 'w') as f:
  json.dump(top_count_openings, f, indent=4)
  
  
for op in top_count_openings:
  print(f"{op['name']['name']:<80}  {op['plays']:<50} {op['count']}")

from pprint import pprint

pprint(OPENINGS_BY_MOVE)