# Mécaniques de Combat

## Table des matières
1. [Vue d'ensemble](#vue-densemble)
2. [Classes de personnages](#classes-de-personnages)
3. [Statistiques](#statistiques)
4. [Système de combat](#système-de-combat)
5. [Capacités spéciales](#capacités-spéciales)
6. [Équipement](#équipement)
7. [Effets et états](#effets-et-états)
8. [Formules de calcul](#formules-de-calcul)

## Vue d'ensemble

Le système de combat est un système au tour par tour basé sur la vitesse des personnages. Chaque personnage possède des statistiques uniques, des capacités spéciales et peut être équipé d'objets améliorant ses performances.

## Classes de personnages

### Guerrier
- **Spécialité**: Combat rapproché
- **Avantage**: Fort contre les Archers
- **Capacités**:
  - Coup Puissant (20 dégâts, ignore la défense)
  - Cri de Guerre (+5 force, +3 défense pour 2 tours)

### Archer
- **Spécialité**: Attaques à distance
- **Avantage**: Fort contre les Mages
- **Capacités**:
  - Tir Précis (25 dégâts)
  - Pluie de Flèches (12 dégâts sur tous les ennemis)

### Mage
- **Spécialité**: Sorts et magie
- **Avantage**: Fort contre les Guerriers
- **Capacités**:
  - Boule de Feu (15 dégâts + 5 dégâts/tour pendant 3 tours)
  - Barrière Magique (+8 défense pour 2 tours)

### Sorceleur
- **Spécialité**: Hybride combat/magie
- **Capacités**:
  - Signe d'Aard (18 dégâts)
  - Signe de Quen (+6 défense pour 2 tours)

## Statistiques

### Statistiques de base
- **Force**: Détermine les dégâts de base
- **Défense**: Réduit les dégâts reçus
- **Vitesse**: Détermine l'ordre des tours
- **Points de vie (HP)**: Santé du personnage

### Modificateurs
- **Moral**: Affecte les performances (-50% à +50%)
- **Fatigue**: Réduit les performances (jusqu'à -50%)

## Système de combat

### Ordre des tours
1. Les personnages agissent dans l'ordre décroissant de leur vitesse
2. À chaque tour, un personnage peut:
   - Effectuer une attaque normale
   - Utiliser une capacité spéciale (si disponible)

### Avantages de classe
- Bonus de +20% aux dégâts contre les classes faibles
- Malus de -20% aux dégâts contre les classes fortes

### Calcul des dégâts

#### Dégâts de base
```
Si force < 10:
    dégâts = 5
Si 10 <= force < 20:
    dégâts = 15
Si 20 <= force < 30:
    dégâts = 20
Sinon:
    dégâts = 25
```

#### Réduction des dégâts
```
Si défense < 5:
    réduction = 0
Si 5 <= défense < 10:
    réduction = 5
Si 10 <= défense < 15:
    réduction = 10
Sinon:
    réduction = 15
```

## Capacités spéciales

### Système de cooldown
- Chaque capacité a un temps de recharge
- Chance de base de 30% d'utilisation quand disponible

### Types d'effets
- **DAMAGE**: Dégâts directs
- **HEAL**: Restauration de PV
- **BUFF_STRENGTH**: Augmentation de force
- **BUFF_DEFENSE**: Augmentation de défense
- **DEBUFF_DEFENSE**: Réduction de défense
- **DOT**: Dégâts sur la durée

## Équipement

### Slots d'équipement
- Main principale (MAIN_HAND)
- Main secondaire (OFF_HAND)
- Tête (HEAD)
- Torse (CHEST)
- Jambes (LEGS)
- Anneau (RING)
- Amulette (AMULET)

### Bonus d'équipement
- Les statistiques sont cumulatives
- Chaque pièce peut affecter:
  - Force
  - Défense
  - Vitesse
  - Points de vie
  - Magie

## Effets et états

### Types d'effets
1. **Effets instantanés**
   - Dégâts
   - Soins

2. **Effets temporaires**
   - Buffs de statistiques
   - Débuffs
   - Dégâts sur la durée

### Durée des effets
- Les effets temporaires durent un nombre spécifique de tours
- Les effets sont mis à jour à la fin de chaque tour

## Formules de calcul

### Modificateur de combat
```python
combat_modifier = 1 + (morale - 50) / 100 + (-fatigue / 200)
```

### Force effective
```python
force_effective = force_base * combat_modifier
```

### Défense effective
```python
défense_effective = défense_base * combat_modifier
```

### Dégâts finaux
```python
dégâts_finaux = max(1, dégâts_base * modificateur_classe - réduction_défense)
``` 