import random

# Dictionnaires
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
weights = {
    'a8': '73', 'b8': '13', 'c8': '859', 'd8': '570', 'e8': '651', 'f8': '948', 'g8': '4', 'h8': '7',
    'a7': '81', 'b7': '232', 'c7': '834', 'd7': '1658', 'e7': '1920', 'f7': '1788', 'g7': '538', 'h7': '87',
    'a6': '74', 'b6': '400', 'c6': '9480', 'd6': '7333', 'e6': '5797', 'f6': '8882', 'g6': '172', 'h6': '101',
    'a5': '172', 'b5': '1518', 'c5': '3507', 'd5': '12986', 'e5': '17182', 'f5': '2574', 'g5': '2085', 'h5': '256',
    'a4': '56', 'b4': '1668', 'c4': '3940', 'd4': '8946', 'e4': '4713', 'f4': '6518', 'g4': '1527', 'h4': '58',
    'a3': '3', 'b3': '16', 'c3': '9811', 'd3': '2242', 'e3': '1744', 'f3': '9414', 'g3': '100', 'h3': '26',
    'a2': '13', 'b2': '459', 'c2': '1041', 'd2': '1926', 'e2': '1665', 'f2': '2038', 'g2': '1434', 'h2': '34',
    'a1': '1083', 'b1': '3', 'c1': '1099', 'd1': '559', 'e1': '585', 'f1': '667', 'g1': '37', 'h1': '1317',
}
import random

# Sélectionner une case en tenant compte des poids
def choisir_case_ponderee(system, weights):
    cases = list(system.keys())
    poids = [int(weights[case]) for case in cases]
    return random.choices(cases, weights=poids, k=1)[0]

# Générer une question
def generate_question(white_system, black_system, weights):
    # Choisir aléatoirement entre système blanc ou noir
    system = random.choice([(white_system, "blanc"), (black_system, "noir")])
    system_dict = system[0]
    
    # Sélectionner une case pondérée
    case = choisir_case_ponderee(system_dict, weights)
    
    return {
        "system": system[1],
        "case": case,
        "reponse": system_dict[case]
    }

# Fonction de jeu principale
def jouer_partie(white_system, black_system, weights, nombre_questions=5):
    score = 0
    questions_posees = []
    
    print("\nBienvenue dans le jeu d'apprentissage des cases d'échecs!")
    print(f"Vous allez avoir {nombre_questions} questions. Répondez le plus précisément possible.\n")
    
    for i in range(nombre_questions):
        question = generate_question(white_system, black_system, weights)
        questions_posees.append(question)
        
        print(f"\nQuestion {i+1}/{nombre_questions}:")
        print(f"Quel mot se trouve sur la case {question['case']} {question['system']}?")
        
        reponse_utilisateur = input("Votre réponse: ").lower().strip()
        reponse_correcte = question["reponse"].lower()
        
        if reponse_utilisateur == reponse_correcte:
            print("Correct! +1 point")
            score += 1
        else:
            print(f"Incorrect. La bonne réponse était: {question['reponse']}")
    
    # Afficher le résultat final
    print(f"\nFin du jeu! Votre score: {score}/{nombre_questions}")
    if score == nombre_questions:
        print("Parfait! Vous avez tout bon!")
    elif score >= nombre_questions * 0.7:
        print("Très bien! Continuez comme ça!")
    else:
        print("Continuez à pratiquer!")
    
    # Proposer de revoir les erreurs
    if score < nombre_questions:
        revoir = input("\nVoulez-vous revoir les questions manquées? (oui/non): ")
        if revoir.lower().strip() == "oui":
            print("\nQuestions manquées:")
            for q in questions_posees:
                print(f"Case {q['case']} {q['system']}: {q['reponse']}")

# Fonction principale pour lancer le jeu
def main():
    while True:
        nb_questions = input("\nCombien de questions voulez-vous? (5 par défaut): ")
        try:
            nb_questions = int(nb_questions) if nb_questions else 5
            jouer_partie(white_system, black_system, weights, nb_questions)
        except ValueError:
            print("Nombre invalide, utilisation de la valeur par défaut (5)")
            jouer_partie(white_system, black_system, weights)
            
        rejouer = input("\nVoulez-vous rejouer? (oui/non): ")
        if rejouer.lower().strip() != "oui":
            print("Merci d'avoir joué!")
            break

if __name__ == "__main__":
    main()