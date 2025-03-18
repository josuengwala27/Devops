# main.py

from characters import Character
from combat import combat_start

# Configuration manuelle des équipes
team1 = [
    Character("Guerrier1", speed=5),
    Character("Archer1", speed=7),
    Character("Mage1", speed=4)
]

team2 = [
    Character("Guerrier2", speed=6),
    Character("Archer2", speed=8),
    Character("Mage2", speed=3)
]

# Affichage pour vérification
print("Équipe 1 :")
for c in team1:
    print(c)

print("\nÉquipe 2 :")
for c in team2:
    print(c)

combat_start(team1, team2)