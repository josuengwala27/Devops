# combat.py

def combat_start(team1, team2):
    print("\n--- Début du combat ---\n")

    # Fusion des deux équipes et tri des personnages par vitesse décroissante
    all_characters = team1 + team2
    all_characters.sort(key=lambda c: c.speed, reverse=True)

    print("Ordre d'attaque (par vitesse) :")
    for c in all_characters:
        print(f"{c.name} (Vitesse : {c.speed})")

    print("\n(La logique d'attaque arrive bientôt !)\n")