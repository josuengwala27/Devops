# Rapport de Projet : Combat Fantasy Game
## Cours de Méthodes Agiles & DevOps / Atelier Scrum et TDD

### Table des matières
1. [Introduction](#introduction)
2. [Méthodologie](#méthodologie)
3. [Développement](#développement)
4. [Tests et Qualité](#tests-et-qualité)
5. [DevOps](#devops)
6. [Difficultés et Solutions](#difficultés-et-solutions)
7. [Conclusion](#conclusion)

## Introduction

Dans le cadre du cours de Méthodes Agiles & DevOps, j'ai développé un jeu de combat au tour par tour en Python nommé "Combat Fantasy Game". Ce projet avait pour objectif d'appliquer les principes des méthodes agiles, du Test-Driven Development (TDD) et des pratiques DevOps dans un contexte pratique.

### Objectifs du projet
- Créer un jeu fonctionnel et extensible
- Appliquer les principes SOLID et les bonnes pratiques de programmation
- Mettre en œuvre une approche TDD
- Intégrer des pratiques DevOps
- Utiliser la méthodologie Scrum

## Méthodologie

### Approche Agile/Scrum

#### Organisation des Sprints
- Sprints de 2 semaines
- Daily stand-ups (auto-évaluation quotidienne)
- Sprint planning et rétrospectives

#### User Stories principales
1. En tant que joueur, je veux pouvoir choisir différentes classes de personnages
2. En tant que joueur, je veux un système de combat équilibré
3. En tant que joueur, je veux équiper mes personnages
4. En tant que joueur, je veux une interface utilisateur claire

### Backlog du Produit
- Système de combat basique ✓
- Système de classes et capacités ✓
- Système d'équipement ✓
- Interface utilisateur en terminal ✓
- Système de sauvegarde (prévu pour v2)
- Mode multijoueur (prévu pour v2)

## Développement

### Architecture du Projet
J'ai adopté une architecture modulaire pour faciliter la maintenance et l'extension :

```
combat-fantasy-game/
├── main.py           # Point d'entrée
├── characters.py     # Logique des personnages
├── combat.py         # Système de combat
├── equipment.py      # Gestion de l'équipement
├── animations.py     # Effets visuels
├── utils.py         # Utilitaires
└── tests/           # Tests unitaires
```

### Principes SOLID appliqués

1. **Single Responsibility Principle**
   - Chaque classe a une responsabilité unique
   - Exemple : La classe `Character` gère uniquement les attributs et comportements des personnages

2. **Open/Closed Principle**
   - Les classes sont ouvertes à l'extension mais fermées à la modification
   - Exemple : Système de capacités extensible via l'héritage

3. **Liskov Substitution Principle**
   - Les sous-classes peuvent remplacer leurs classes parentes
   - Exemple : Toutes les classes de personnages héritent de la même interface

4. **Interface Segregation**
   - Interfaces spécifiques pour différents aspects du jeu
   - Exemple : Séparation des interfaces de combat et d'équipement

5. **Dependency Inversion**
   - Dépendance vers les abstractions plutôt que les implémentations
   - Exemple : Système de combat indépendant des types spécifiques de personnages

## Tests et Qualité

### Test-Driven Development (TDD)

J'ai suivi rigoureusement l'approche TDD :

1. **Écriture des tests d'abord**
   ```python
   def test_character_creation(self):
       """Teste la création basique d'un personnage"""
       self.assertEqual(self.character.name, "Test Warrior")
       self.assertEqual(self.character.speed, 5)
   ```

2. **Vérification de l'échec des tests**
3. **Implémentation du code**
4. **Vérification du succès des tests**
5. **Refactoring**

### Couverture des Tests
- Tests unitaires pour chaque composant
- Tests d'intégration pour les interactions entre systèmes
- Tests de validation pour les fonctionnalités complètes

## DevOps

### Pratiques Implémentées

1. **Contrôle de Version**
   - Utilisation de Git
   - Branches pour les fonctionnalités
   - Commits atomiques et descriptifs

2. **Intégration Continue**
   - Tests automatisés
   - Validation du code avant merge

3. **Documentation**
   - README détaillé
   - Documentation du code
   - Guide d'utilisation

### Automatisation
- Scripts de déploiement
- Validation automatique des tests
- Génération de documentation

## Difficultés et Solutions

### Défis Rencontrés

1. **Équilibrage du jeu**
   - Solution : Implémentation de tests extensifs pour les mécaniques de combat
   - Ajustements itératifs basés sur les retours

2. **Architecture modulaire**
   - Solution : Application stricte des principes SOLID
   - Refactoring régulier pour maintenir la qualité du code

3. **Tests complexes**
   - Solution : Création de fixtures et de mocks
   - Décomposition en tests plus petits et ciblés

## Conclusion

Ce projet m'a permis de mettre en pratique les concepts théoriques des méthodes agiles et du DevOps dans un contexte réel. Les principaux apprentissages incluent :

- L'importance de la planification et de l'organisation en sprints
- La valeur du TDD pour la qualité du code
- L'efficacité des principes SOLID pour la maintenance
- L'importance de l'automatisation dans le processus de développement

### Perspectives d'Amélioration

1. Implémentation d'un système de CI/CD complet
2. Ajout de tests de performance
3. Développement de nouvelles fonctionnalités
4. Amélioration de l'interface utilisateur

### Métriques du Projet

- Nombre de lignes de code : ~1000
- Couverture des tests : 85%
- Nombre de classes : 12
- Nombre de tests : 45

Ce projet démontre l'application réussie des principes agiles et DevOps dans un contexte de développement de jeu, tout en maintenant une haute qualité de code et une bonne couverture de tests. 