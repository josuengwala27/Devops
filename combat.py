# combat.py
import random
import time
from colorama import Fore, Style, init

# Initialisation de colorama pour Windows
init(autoreset=True)

def combat_start(team1, team2):
    print(Fore.YELLOW + "\n🏰 --- DÉBUT DU COMBAT --- 🏰\n")

    all_characters = team1 + team2
    all_characters.sort(key=lambda c: c.speed, reverse=True)

    round_count = 1
    while any(c.is_alive() for c in team1) and any(c.is_alive() for c in team2):
        print(Fore.CYAN + f"\n⚔️ --- ROUND {round_count} --- ⚔️")
        time.sleep(1)
        for attacker in all_characters:
            if not attacker.is_alive():
                continue

            target_team = team2 if attacker in team1 else team1
            alive_targets = [c for c in target_team if c.is_alive()]

            if not alive_targets:
                break

            target = random.choice(alive_targets)
            roll = random.randint(1, 100)

            if roll <= 5:
                # Coup critique
                damage = 20
                target.hp -= damage
                print(Fore.RED + f"💥 {attacker.name.upper()} réalise un COUP CRITIQUE sur {target.name} ! (-{damage} HP)")
            elif roll >= 96:
                # Fumble
                attacker.hp -= 10
                print(Fore.MAGENTA + f"🤦 {attacker.name} trébuche et s'auto-inflige 10 HP !")
            else:
                damage = random.randint(0, 10)
                color = Fore.GREEN if damage <= 5 else Fore.LIGHTRED_EX
                print(color + f"{attacker.name} attaque {target.name} et inflige {damage} HP.")
                target.hp -= damage

            time.sleep(0.7)

        round_count += 1
        time.sleep(1)

    # Fin du combat
    print(Fore.YELLOW + "\n🏆 --- FIN DU COMBAT --- 🏆")
    winner = "Équipe 1" if any(c.is_alive() for c in team1) else "Équipe 2"
    print(Fore.LIGHTGREEN_EX + f"\n🎉 VICTOIRE DE {winner} ! 🎉\n")

    print(Fore.CYAN + "État final des personnages :")
    for c in all_characters:
        status = Fore.LIGHTGREEN_EX + "Vivant" if c.is_alive() else Fore.LIGHTBLACK_EX + "Mort"
        print(f"{c.name} - {status} ({c.hp} HP)")

