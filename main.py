# main.py

from characters import Character
from combat import combat_start, print_team_status
from colorama import Fore
from utils import get_terminal_size, create_responsive_format, create_border, create_box, center_text, create_separator
import time
import sys
from random import choice

# Configuration manuelle des équipes avec des classes et attributs variés
team1 = [
    Character("Aragorn", speed=5, strength=15, defense=8, character_class="Guerrier"),
    Character("Legolas", speed=7, strength=12, defense=4, character_class="Archer"),
    Character("Gandalf", speed=4, strength=18, defense=6, character_class="Mage")
]

team2 = [
    Character("Geralt", speed=6, strength=14, defense=7, character_class="Sorceleur"),
    Character("Hawkeye", speed=8, strength=11, defense=3, character_class="Archer"),
    Character("Merlin", speed=3, strength=17, defense=5, character_class="Mage")
]

def print_slow(text, delay=0.03):
    """Affiche le texte caractère par caractère"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_animation(text, duration=2):
    """Affiche une animation de chargement"""
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{animation[i]} {text}")
        sys.stdout.flush()
        time.sleep(0.1)
        i = (i + 1) % len(animation)
    print()

def display_title_screen():
    """Affiche un écran titre animé"""
    terminal_width = get_terminal_size()
    title_art = [
        "█▀▀ █▀█ █▀▄▀█ █▄▄ ▄▀█ ▀█▀   █▀█ █▀█ █▀▀",
        "█▄▄ █▄█ █░▀░█ █▄█ █▀█ ░█░   █▀▄ █▀▀ █▄█",
        "    █▀▀ ▄▀█ █▄░█ ▀█▀ ▄▀█ █▀ █▄█",
        "    █▀░ █▀█ █░▀█ ░█░ █▀█ ▄█ ░█░"
    ]
    
    print("\n" * 3)
    for line in title_art:
        print(Fore.CYAN + center_text(line, terminal_width))
        time.sleep(0.2)
    print("\n")
    
    loading_animation("Chargement du jeu", 2)
    print("\n" * 2)

display_title_screen()

# Configuration manuelle des équipes avec des classes et attributs variés
print_slow(Fore.CYAN + "Initialisation des équipes..." + Fore.RESET)
time.sleep(0.5)

# Création d'une bannière pour la présentation des équipes
terminal_width = get_terminal_size()
print(create_box("⚔️  PRÉSENTATION DES ÉQUIPES  ⚔️", terminal_width - 4, "double"))
print("\n")

# Affichage amélioré des équipes
print_team_status(team1, "✦ ÉQUIPE DES HÉROS ✦")
print("\n" + create_separator(terminal_width - 4, "stars") + "\n")
print_team_status(team2, "❖ ÉQUIPE DES CHALLENGERS ❖")

# Configuration du jeu avec une interface améliorée
print("\n" + create_box("🎮 CONFIGURATION DE LA PARTIE", terminal_width - 4, "double") + "\n")

# Menu de vitesse amélioré
speed_menu = [
    "╔" + "═" * (terminal_width - 6) + "╗",
    "║" + center_text("🕒 VITESSE DU JEU", terminal_width - 6) + "║",
    "╠" + "═" * (terminal_width - 6) + "╣",
    "║" + center_text("1. 🐌 Lent (0.5x)", terminal_width - 6) + "║",
    "║" + center_text("2. 🚶 Normal (1x)", terminal_width - 6) + "║",
    "║" + center_text("3. 🏃 Rapide (2x)", terminal_width - 6) + "║",
    "║" + center_text("4. ⚡ Très rapide (3x)", terminal_width - 6) + "║",
    "╚" + "═" * (terminal_width - 6) + "╝"
]

for line in speed_menu:
    print(Fore.CYAN + line)

while True:
    try:
        choice = int(input(Fore.YELLOW + "\n➤ Votre choix (1-4) : " + Fore.WHITE))
        if 1 <= choice <= 4:
            break
        print(Fore.RED + "⚠ Veuillez entrer un nombre entre 1 et 4")
    except ValueError:
        print(Fore.RED + "⚠ Veuillez entrer un nombre valide")

speed_options = {1: 0.5, 2: 1.0, 3: 2.0, 4: 3.0}
game_speed = speed_options[choice]

# Configuration du nombre de rounds avec interface améliorée
print("\n" + create_box("🎯 NOMBRE DE ROUNDS", terminal_width - 4, "single"))
rounds_menu = [
    "│" + center_text("0. 🔄 Mode sans limite", terminal_width - 6) + "│",
    "│" + center_text("n. 🎯 Nombre spécifique de rounds", terminal_width - 6) + "│",
    "└" + "─" * (terminal_width - 6) + "┘"
]

for line in rounds_menu:
    print(Fore.CYAN + line)

while True:
    try:
        max_rounds = int(input(Fore.YELLOW + "\n➤ Entrez le nombre de rounds (0 = sans limite) : " + Fore.WHITE))
        if max_rounds >= 0:
            break
        print(Fore.RED + "⚠ Veuillez entrer un nombre positif")
    except ValueError:
        print(Fore.RED + "⚠ Veuillez entrer un nombre valide")

max_rounds = None if max_rounds == 0 else max_rounds

# Résumé de la configuration
print("\n" + create_box("📋 RÉSUMÉ DE LA CONFIGURATION", terminal_width - 4, "double"))
config_summary = [
    "║" + center_text(f"⚡ Vitesse de jeu : {game_speed}x", terminal_width - 6) + "║",
    "║" + center_text(f"🎯 Nombre de rounds : {'Illimité' if max_rounds is None else max_rounds}", terminal_width - 6) + "║",
    "╚" + "═" * (terminal_width - 6) + "╝"
]

for line in config_summary:
    print(Fore.GREEN + line)

print(Fore.YELLOW + "\n" + center_text("Appuyez sur Entrée pour commencer le combat...", terminal_width))
input()

# Affichage d'une animation de début de combat
print("\n" + create_separator(terminal_width, "stars"))
print(Fore.RED + center_text("⚔️  QUE LE COMBAT COMMENCE  ⚔️", terminal_width))
print(create_separator(terminal_width, "stars") + "\n")

def display_character_card(character):
    """Affiche une carte de personnage stylisée"""
    card = [
        "╔════════════════════════╗",
        f"║ {character.name:<18} ║",
        "╠════════════════════════╣",
        f"║ Classe: {character.character_class:<13} ║",
        f"║ Force : {character.strength:<13} ║",
        f"║ Déf   : {character.defense:<13} ║",
        f"║ Vit.  : {character.speed:<13} ║",
        "╚════════════════════════╝"
    ]
    return card

def display_teams(team1, team2):
    """Affiche les équipes de manière plus élaborée côte à côte"""
    terminal_width = get_terminal_size()
    team_width = (terminal_width - 4) // 2  # Espace pour deux équipes

    print("\n" + create_separator(terminal_width, "stars"))
    print(Fore.YELLOW + center_text("⚔️  PRÉSENTATION DES ÉQUIPES  ⚔️", terminal_width))
    print(create_separator(terminal_width, "stars") + "\n")
    
    # Préparer les cartes des deux équipes
    team1_cards = []
    team2_cards = []
    
    for char in team1:
        team1_cards.extend(display_character_card(char))
    for char in team2:
        team2_cards.extend(display_character_card(char))
    
    # Afficher les titres
    print(Fore.CYAN + center_text("✦ ÉQUIPE DES HÉROS ✦", team_width) + 
          "  " + 
          Fore.RED + center_text("❖ ÉQUIPE DES CHALLENGERS ❖", team_width))
    print()
    
    # Afficher les cartes côte à côte
    max_lines = max(len(team1_cards), len(team2_cards))
    for i in range(0, max_lines, 9):  # 9 est la hauteur d'une carte
        # Afficher 8 lignes (une carte complète)
        for j in range(8):
            if i+j < len(team1_cards):
                line1 = team1_cards[i+j]
            else:
                line1 = " " * 30  # Largeur approximative d'une carte
                
            if i+j < len(team2_cards):
                line2 = team2_cards[i+j]
            else:
                line2 = " " * 30
                
            print(Fore.CYAN + center_text(line1, team_width) + 
                  "  " + 
                  Fore.RED + center_text(line2, team_width))
        
        # Ajouter un espace entre les cartes
        if i + 8 < max_lines:
            print()

display_teams(team1, team2)

def display_combat_start_animation():
    """Affiche une animation de début de combat"""
    terminal_width = get_terminal_size()
    animations = [
        "⚔️  PRÉPAREZ-VOUS AU COMBAT  ⚔️",
        "🗡️  LES ÉPÉES S'ENTRECHOQUENT  🗡️",
        "✨  LA MAGIE CRÉPITE  ✨",
        "🏹  LES ARCHERS SONT PRÊTS  🏹"
    ]
    
    print("\n" + create_separator(terminal_width, "stars"))
    for anim in animations:
        # Suppression des espaces superflus et centrage précis
        print(Fore.YELLOW + center_text(anim.strip(), terminal_width))
        time.sleep(0.7)
    print(create_separator(terminal_width, "stars") + "\n")

# Supprimer la répétition du titre "QUE LE COMBAT COMMENCE"
display_combat_start_animation()

# Afficher directement le début des rounds
print(Fore.CYAN + "\n" + create_box("🎮 DÉBUT DES ROUNDS", terminal_width - 4, "double") + "\n")

combat_start(team1, team2, game_speed, max_rounds)