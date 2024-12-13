import random

# Dictionnaires
white_system = {
    'c6': 'bambi', 'd6': 'obélix', 'e6': 'aquaman', 'f6': 'batman',
    'c5': 'jungle', 'd5': 'napoléon', 'e5': 'jésus', 'f5': 'désert',
    'c4': 'chateau', 'd4': 'goku', 'e4': 'simba', 'f4': 'montagne',
    'c3': 'léonidas', 'd3': 'thanos', 'e3': 'merlin', 'f3': 'lancelot',
}

black_system = {
    'c6': 'bondir', 'd6': 'porter', 'e6': 'nager', 'f6': 'traquer',
    'c5': 'cacher', 'd5': 'conquérir', 'e5': 'prier', 'f5': 'seul',
    'c4': 'fort', 'd4': 'voler', 'e4': 'rugir', 'f4': 'escalader',
    'c3': 'défendre', 'd3': 'anéantir', 'e3': 'enchanter', 'f3': 'chevaucher'
}
weights = {
    'c6': '9480', 'd6': '7333', 'e6': '5797', 'f6': '8882',
    'c5': '3507', 'd5': '12986', 'e5': '17182', 'f5': '2574',
    'c4': '3940', 'd4': '8946', 'e4': '4713', 'f4': '6518',
    'c3': '9811', 'd3': '2242', 'e3': '1744', 'f3': '9414'
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