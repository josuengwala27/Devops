# combat.py
import random
import time
from colorama import Fore, Style, init
from utils import get_terminal_size, create_responsive_format, create_border, center_text, create_separator

# Initialisation de colorama pour Windows
init(autoreset=True)

def create_health_bar(current_hp, max_hp=100, bar_length=20):
    # Ajuster la longueur de la barre en fonction de la largeur du terminal
    terminal_width = get_terminal_size()
    bar_length = min(bar_length, terminal_width // 4)  # Limite la taille de la barre
    
    filled_length = int(bar_length * current_hp / max_hp)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    percentage = current_hp / max_hp * 100
    return f"[{bar}] {int(percentage)}%"

def print_team_status(team, team_name):
    print(Fore.CYAN + f"✧ {team_name} ✧")
    print(Fore.CYAN + "─────────────────────────────")
    for char in team:
        class_emoji = {
            "Guerrier": "⚔️",
            "Archer": "🏹",
            "Mage": "🔮",
            "Sorceleur": "⚡"
        }.get(char.character_class, "❓")
        
        # Ligne 1: Nom et classe
        print(Fore.WHITE + f"  {class_emoji} {char.name} - {char.character_class}")
        # Ligne 2: Stats avec émojis
        print(Fore.LIGHTBLUE_EX + f"  ⚡ Vitesse: {char.speed} │ 💪 Force: {char.strength} │ 🛡️ Défense: {char.defense}")
        # Ligne 3: Barre de vie
        health_bar = create_health_bar(char.hp)
        print(Fore.GREEN + f"  ❤️ {health_bar}")
        print(Fore.CYAN + "  · · · · · · · · · · · · · · ·")

def combat_start(team1, team2, game_speed=1.0, max_rounds=None):
    """
    game_speed: float - vitesse du jeu
    max_rounds: int - nombre maximum de rounds (None = pas de limite)
    """
    # Affichage du titre
    print(Fore.YELLOW + "\n" + "•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°")
    print(Fore.YELLOW + "           ⚔️  DÉBUT DU COMBAT  ⚔️")
    print(Fore.YELLOW + "•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°\n")

    # Affichage des équipes au début
    print_team_status(team1, "ÉQUIPE 1")
    print()  # Espace entre les équipes
    print_team_status(team2, "ÉQUIPE 2")
    
    print(Fore.YELLOW + "\n" + "•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°")
    print(Fore.YELLOW + "          🎮 QUE LE COMBAT COMMENCE!")
    print(Fore.YELLOW + "•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°\n")
    
    all_characters = team1 + team2
    all_characters.sort(key=lambda c: c.speed, reverse=True)
    round_count = 1
    
    while any(c.is_alive() for c in team1) and any(c.is_alive() for c in team2):
        if max_rounds and round_count > max_rounds:
            break

        # Affichage du round
        print(Fore.CYAN + f"\n🔄 ROUND {round_count}/{max_rounds if max_rounds else '∞'}")
        print(Fore.CYAN + "=" * 50)
        
        for attacker in all_characters:
            if not attacker.is_alive():
                continue

            target_team = team2 if attacker in team1 else team1
            alive_targets = [c for c in target_team if c.is_alive()]
            if not alive_targets:
                break

            target = random.choice(alive_targets)
            roll = random.randint(1, 100)
            
            # Ligne de séparation
            print(Fore.WHITE + "-" * 50)
            
            # Affichage de l'attaquant avec son emoji de classe
            attacker_emoji = {
                "Guerrier": "⚔️",
                "Archer": "🏹",
                "Mage": "🔮",
                "Sorceleur": "⚡"
            }.get(attacker.character_class, "❓")
            print(Fore.WHITE + f"{attacker_emoji} {attacker.name} | 🎲 Dé: {roll}")
            
            if roll <= 5:
                base_damage = attacker.strength * 2
                actual_damage = target.take_damage(base_damage)
                print(Fore.RED + f"💥 COUP CRITIQUE! {target.name} subit {actual_damage} dégâts!")
            elif roll >= 96:
                attacker.take_damage(10)
                print(Fore.MAGENTA + f"💫 ÉCHEC CRITIQUE! {attacker.name} se blesse (-10 HP)")
            else:
                base_damage = random.randint(1, attacker.strength)
                actual_damage = target.take_damage(base_damage)
                color = Fore.GREEN if actual_damage <= 5 else Fore.LIGHTRED_EX
                print(color + f"⚔️ ATTAQUE: {target.name} subit {actual_damage} dégâts")

            # Affichage de la barre de vie si nécessaire
            if roll >= 96 or actual_damage > 0:
                char_to_display = attacker if roll >= 96 else target
                health_bar = create_health_bar(char_to_display.hp)
                print(Fore.CYAN + f"❤️ Vie de {char_to_display.name}: {health_bar}")

            time.sleep(0.5 / game_speed)

        print(Fore.CYAN + "=" * 50)
        round_count += 1
        time.sleep(0.5 / game_speed)

    # Affichage des résultats finaux
    if max_rounds and round_count > max_rounds:
        display_final_results(team1, team2, "⌛ MATCH NUL PAR LIMITE DE ROUNDS!")
    else:
        winner_team = "✦ ÉQUIPE DES HÉROS ✦" if any(c.is_alive() for c in team1) else "❖ ÉQUIPE DES CHALLENGERS ❖"
        display_final_results(team1, team2, f"🎉 VICTOIRE DE {winner_team} 🎉")

def health_bar(percentage, width=20):
    """Crée une barre de vie visuelle"""
    filled = int(width * percentage / 100)
    bar = "█" * filled + "░" * (width - filled)
    return bar

def display_final_results(team1, team2, result="MATCH NUL"):
    """Affiche un écran final stylisé avec les résultats"""
    terminal_width = get_terminal_size()
    
    # Bannière de fin
    print("\n" + "═" * terminal_width)
    print(Fore.YELLOW + center_text("🏆 RÉSULTATS DU COMBAT 🏆", terminal_width))
    print("═" * terminal_width + "\n")
    
    # Affichage du résultat
    result_box = [
        "╔" + "═" * (terminal_width - 2) + "╗",
        "║" + center_text(result, terminal_width - 2) + "║",
        "╚" + "═" * (terminal_width - 2) + "╝"
    ]
    for line in result_box:
        print(Fore.YELLOW + line)
    
    print("\n" + create_separator(terminal_width, "stars") + "\n")
    
    # Statistiques des équipes
    print(Fore.CYAN + center_text("📊 STATISTIQUES FINALES 📊", terminal_width) + "\n")
    
    # Affichage côte à côte des équipes
    team_width = (terminal_width - 6) // 2
    
    def create_team_stats(team, title):
        stats = []
        stats.append("╔" + "═" * (team_width - 2) + "╗")
        stats.append("║" + center_text(title, team_width - 2) + "║")
        stats.append("╠" + "═" * (team_width - 2) + "╣")
        
        for i, char in enumerate(team):
            health_percent = int((char.hp / char.max_hp) * 100)
            color = (Fore.GREEN if health_percent > 50 
                    else Fore.YELLOW if health_percent > 25 
                    else Fore.RED)
            
            stats.append("║" + center_text(f"{char.name} ({char.character_class})", team_width - 2) + "║")
            stats.append("║" + center_text(f"❤️ Vie: {char.hp}/{char.max_hp} ({health_percent}%)", team_width - 2) + "║")
            stats.append("║" + center_text(health_bar(health_percent, 20), team_width - 2) + "║")
            if i < len(team) - 1:
                stats.append("║" + "─" * (team_width - 2) + "║")
        
        stats.append("╚" + "═" * (team_width - 2) + "╝")
        return stats
    
    # Création des statistiques pour chaque équipe
    team1_stats = create_team_stats(team1, "✦ ÉQUIPE DES HÉROS ✦")
    team2_stats = create_team_stats(team2, "❖ ÉQUIPE DES CHALLENGERS ❖")
    
    # Affichage côte à côte en une seule fois
    max_lines = max(len(team1_stats), len(team2_stats))
    for i in range(max_lines):
        line1 = team1_stats[i] if i < len(team1_stats) else " " * team_width
        line2 = team2_stats[i] if i < len(team2_stats) else " " * team_width
        print(Fore.CYAN + line1 + "  " + Fore.RED + line2)
    
    # Bannière de fin
    print("\n" + create_separator(terminal_width, "stars"))
    print(Fore.YELLOW + center_text("🎮 FIN DE LA PARTIE 🎮", terminal_width))
    print(create_separator(terminal_width, "stars") + "\n")

