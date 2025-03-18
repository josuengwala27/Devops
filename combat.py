# combat.py

def combat_start(team1, team2):
    print("\n--- Début du combat ---\n")
    print("Équipe 1 :")
    for c in team1:
        print(f"{c.name} (HP: {c.hp}, Speed: {c.speed})")

    print("\nÉquipe 2 :")
    for c in team2:
        print(f"{c.name} (HP: {c.hp}, Speed: {c.speed})")

    print("\nLe combat va commencer...\n")