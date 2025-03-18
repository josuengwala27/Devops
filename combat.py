# combat.py
import random
import time

def combat_start(team1, team2):
    print("\n--- Début du combat ---\n")

    all_characters = team1 + team2
    all_characters.sort(key=lambda c: c.speed, reverse=True)

    round_count = 1
    while any(c.is_alive() for c in team1) and any(c.is_alive() for c in team2):
        print(f"\n--- Round {round_count} ---")
        for attacker in all_characters:
            if not attacker.is_alive():
                continue  # Sauter si personnage KO

            # Déterminer l’équipe adverse
            target_team = team2 if attacker in team1 else team1
            alive_targets = [c for c in target_team if c.is_alive()]

            if not alive_targets:
                break  # L'équipe adverse est vaincue

            target = random.choice(alive_targets)

            # Calcul des dégâts
            roll = random.randint(1, 100)
            if roll <= 5:
                # Coup critique
                damage = 20
                target.hp -= damage
                print(f"💥 {attacker.name} fait un CRITIQUE sur {target.name} ! -{damage} HP")
            elif roll >= 96:
                # Fumble critique
                attacker.hp -= 10
                print(f"🤦 {attacker.name} rate son attaque et s'auto-inflige 10 HP !")
            else:
                damage = random.randint(0, 10)
                target.hp -= damage
                print(f"{attacker.name} attaque {target.name} pour {damage} HP.")

            # Pause courte pour lisibilité
            time.sleep(0.5)

        round_count += 1

    # Résultat final
    print("\n--- Fin du combat ---")
    winner = "Équipe 1" if any(c.is_alive() for c in team1) else "Équipe 2"
    print(f"🏆 Victoire de {winner} !\n")

    print("État final des personnages :")
    for c in all_characters:
        status = "Vivant" if c.is_alive() else "Mort"
        print(f"{c.name} - {status} ({c.hp} HP)")

