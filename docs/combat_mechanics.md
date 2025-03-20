# Mécaniques de Combat - Documentation

## Système de Combat

### Statistiques de Base
- Force (STR): Détermine les dégâts de base
- Défense (DEF): Réduit les dégâts reçus
- Vitesse (SPD): Détermine l'ordre d'action
- Points de vie (HP): Santé du personnage

### Modificateurs de Combat
1. **Moral (0-100)**
   - Influence les performances au combat
   - > 50 : bonus aux stats
   - < 50 : malus aux stats

2. **Fatigue (0-100)**
   - Augmente pendant le combat
   - Réduit l'efficacité des actions

3. **Avantages de Classe**
   - Guerrier > Archer (+20% dégâts)
   - Archer > Mage (+20% dégâts)
   - Mage > Guerrier (+20% dégâts)

### Capacités Spéciales
Chaque classe possède des capacités uniques avec:
- Cooldown
- Chance d'activation
- Effets spéciaux (dégâts, buffs, etc.)

### Équipement
Les personnages peuvent équiper:
- Arme principale (Main_Hand)
- Armure (Chest)
- Accessoires (Ring, Amulet)
- Casque (Head)

## Déroulement du Combat
1. Initiative basée sur la vitesse
2. Actions possibles:
   - Attaque normale
   - Capacité spéciale
3. Calcul des dégâts:
   - Base = Force de l'attaquant
   - Réduction = Défense du défenseur
   - Modificateurs = Classe + Moral + Fatigue 