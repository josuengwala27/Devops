# main.py

from characters import Character
from combat import combat_start

# Configuration manuelle des équipes
team1 = [
    Character("Aragorn", speed=5),    # Guerrier légendaire
    Character("Legolas", speed=7),    # Archer elfique
    Character("Gandalf", speed=4)     # Mage puissant
]

team2 = [
    Character("Geralt", speed=6),     # Le sorceleur
    Character("Hawkeye", speed=8),    # Archer expert
    Character("Merlin", speed=3)      # Mage mythique
]

# Affichage pour vérification
print("Équipe 1 :")
for c in team1:
    print(c)

print("\nÉquipe 2 :")
for c in team2:
    print(c)

input("\nAppuyez sur Entrée pour commencer le combat...")
combat_start(team1, team2)