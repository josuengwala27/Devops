# Combat Fantasy Game 🎮

Un jeu de combat au tour par tour en Python avec des éléments de RPG, des classes de personnages uniques et un système d'équipement.

## 📋 Table des matières
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancement du jeu](#lancement-du-jeu)
- [Comment jouer](#comment-jouer)
- [Fonctionnalités](#fonctionnalités)
- [Structure du projet](#structure-du-projet)
- [Tests](#tests)
- [Contribution](#contribution)

## ⚙️ Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Terminal supportant les caractères Unicode

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/combat-fantasy-game.git
cd combat-fantasy-game
```

2. Créez un environnement virtuel (recommandé) :
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 🎮 Lancement du jeu

1. Assurez-vous d'être dans le répertoire du projet
2. Activez l'environnement virtuel si ce n'est pas déjà fait
3. Lancez le jeu :
```bash
python main.py
```

## 📖 Comment jouer

1. **Configuration de la partie**
   - Choisissez la vitesse du jeu (0.5x à 3x)
   - Définissez le nombre de rounds (0 pour illimité)

2. **Pendant le combat**
   - Les personnages agissent selon leur vitesse
   - Les attaques et capacités sont utilisées automatiquement
   - Suivez le déroulement du combat dans le terminal

3. **Fin de partie**
   - Le vainqueur est déterminé par l'équipe survivante
   - En cas de limite de rounds, l'équipe avec le plus de PV gagne

## ✨ Fonctionnalités

- **4 Classes uniques** :
  - 🗡️ Guerrier
  - 🏹 Archer
  - 🔮 Mage
  - ⚡ Sorceleur

- **Système de combat élaboré** :
  - Avantages/désavantages entre classes
  - Capacités spéciales
  - Effets sur la durée
  - Système de moral et fatigue

- **Équipement** :
  - 7 slots d'équipement
  - Bonus de statistiques
  - Équipement par classe

- **Interface** :
  - Animations ASCII
  - Barres de vie colorées
  - Affichage des statistiques
  - Messages de combat détaillés

## 📁 Structure du projet

```
combat-fantasy-game/
├── main.py           # Point d'entrée du jeu
├── characters.py     # Classes des personnages
├── combat.py        # Système de combat
├── equipment.py     # Système d'équipement
├── animations.py    # Animations visuelles
├── utils.py         # Utilitaires
├── tests/           # Tests unitaires
└── requirements.txt # Dépendances
```

## 🧪 Tests

Pour lancer les tests unitaires :
```bash
python -m unittest discover tests
```

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Crédits

Développé par [Votre nom]

## 📝 Notes de version

### Version 1.0.0
- Version initiale du jeu
- 4 classes de personnages
- Système de combat complet
- Interface en terminal 