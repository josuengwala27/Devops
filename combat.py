# combat.py
import random
import time
from colorama import Fore, Style, init
from utils import get_terminal_size, create_responsive_format, create_border, center_text, create_separator
from typing import List, Optional
from characters import Character, Ability, Effect, EffectType
from animations import magic_sparkle, sword_clash, fire_effect, arrow_shot, healing_effect
import logging

# Initialisation de colorama pour Windows
init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='combat.log'
)

def create_health_bar(current_hp, max_hp, bar_length=20):
    """Crée une barre de vie avec pourcentage"""
    return create_compact_health_bar(current_hp, max_hp, bar_length)

def print_team_status(team, team_name):
    """Affiche le statut de l'équipe sous forme de tableau"""
    terminal_width = get_terminal_size()
    
    # En-tête de l'équipe
    print(Fore.YELLOW + "╔" + "═" * (terminal_width-2) + "╗")
    print(Fore.YELLOW + "║" + center_text(f"✧ {team_name} ✧", terminal_width-2) + "║")
    print(Fore.YELLOW + "╠" + "═" * (terminal_width-2) + "╣")
    
    for char in team:
        # En-tête du personnage
        class_emoji = {
            "Guerrier": "⚔️",
            "Archer": "🏹",
            "Mage": "🔮",
            "Sorceleur": "⚡"
        }.get(char.character_class, "❓")
        
        # Ligne du personnage
        print(Fore.WHITE + "║" + center_text(f"{class_emoji} {char.name} - {char.character_class}", terminal_width-2) + "║")
        print(Fore.YELLOW + "╟" + "─" * (terminal_width-2) + "╢")
        
        # Stats en colonnes
        stats_line = f"║ {'STATISTIQUES':15} │"
        stats_line += f" Vitesse: {char.base_speed:2} (+{char.speed - char.base_speed:2}) = {char.speed:2} │"
        stats_line += f" Force: {char.base_strength:2} (+{char.strength - char.base_strength:2}) = {char.strength:2} │"
        stats_line += f" Défense: {char.base_defense:2} (+{char.defense - char.base_defense:2}) = {char.defense:2}"
        if char.character_class in ["Mage", "Sorceleur"]:
            stats_line += f" │ Magie: {char.base_magic:2} (+{char.magic - char.base_magic:2}) = {char.magic:2}"
        stats_line += " " * (terminal_width - len(stats_line) - 1) + "║"
        print(Fore.CYAN + stats_line)
        
        # Barre de vie
        hp_line = f"║ {'VIE':15} │ {create_compact_health_bar(char.hp, char.max_hp)}"
        hp_line += " " * (terminal_width - len(hp_line) - 1) + "║"
        print(Fore.GREEN + hp_line)
        
        # Équipements en tableau
        print(Fore.YELLOW + "╟" + "─" * (terminal_width-2) + "╢")
        print(Fore.YELLOW + "║ ÉQUIPEMENTS:" + " " * (terminal_width-14) + "║")
        equipped_items = [(slot, item) for slot, item in char.equipment.items() if item is not None]
        if equipped_items:
            for slot, item in equipped_items:
                stats_str = ", ".join(f"{k}: +{v}" for k, v in item.stats.items())
                equip_line = f"║  • {item.name:20} │ {stats_str}"
                equip_line += " " * (terminal_width - len(equip_line) - 1) + "║"
                print(Fore.YELLOW + equip_line)
        
        # Séparateur entre personnages
        print(Fore.YELLOW + "╠" + "═" * (terminal_width-2) + "╣")
    
    # Pied du tableau
    print(Fore.YELLOW + "╚" + "═" * (terminal_width-2) + "╝\n")

def display_class_advantages():
    """Affiche les avantages de classe"""
    print(Fore.YELLOW + "\n╔════════ AVANTAGES DE CLASSE ════════╗")
    print(Fore.GREEN + "║  ⚔️  Guerrier → Fort contre Archer   ║")
    print(Fore.GREEN + "║  🏹 Archer   → Fort contre Mage     ║")
    print(Fore.GREEN + "║  🔮 Mage     → Fort contre Guerrier ║")
    print(Fore.YELLOW + "╚══════════════════════════════════════╝")
    print(Fore.CYAN + "Note: +20% de dégâts contre la classe faible")
    print(Fore.RED + "      -20% de dégâts contre la classe forte\n")

def combat_start(team1, team2, game_speed=1.0, max_rounds=None):
    """Fonction wrapper pour maintenir la compatibilité"""
    combat_system = CombatSystem(team1, team2, game_speed)
    combat_system.start_combat(max_rounds)
    
class CombatSystem:
    def __init__(self, team1: List[Character], team2: List[Character], game_speed: float = 1.0):
        self.team1 = team1
        self.team2 = team2
        self.game_speed = game_speed
        self.stats = {char.name: CombatStats() for char in team1 + team2}
        self.round_count = 0
        # Afficher une seule fois au début
        self.display_initial_teams()

    def display_initial_teams(self):
        """Affiche une seule fois la présentation complète des équipes au début"""
        print(Fore.YELLOW + "\n" + "•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°")
        print(Fore.YELLOW + "           ⚔️  DÉBUT DU COMBAT  ⚔️")
        print(Fore.YELLOW + "•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°\n")
        
        # Afficher les avantages de classe avant les équipes
        display_class_advantages()
        
        print_team_status(self.team1, "ÉQUIPE DES HÉROS")
        print()
        print_team_status(self.team2, "ÉQUIPE DES CHALLENGERS")

    def get_turn_order(self) -> List[Character]:
        """Détermine l'ordre des tours basé sur la vitesse"""
        all_characters = self.team1 + self.team2
        return sorted(
            [char for char in all_characters if char.is_alive()],
            key=lambda c: c.speed,
            reverse=True
        )

    def select_target(self, attacker: Character) -> Optional[Character]:
        """Sélectionne une cible pour l'attaquant"""
        target_team = self.team2 if attacker in self.team1 else self.team1
        alive_targets = [c for c in target_team if c.is_alive()]
        return random.choice(alive_targets) if alive_targets else None

    def start_combat(self, max_rounds=None):
        """Méthode principale de combat"""
        # Ne plus appeler display_combat_start() ni afficher les équipes à nouveau
        while self.are_teams_alive() and not self.is_max_rounds_reached(max_rounds):
            self.process_round()
            
        self.display_final_results()
    
    def are_teams_alive(self):
        """Vérifie si les deux équipes ont encore des membres vivants"""
        return (any(c.is_alive() for c in self.team1) and 
                any(c.is_alive() for c in self.team2))
    
    def is_max_rounds_reached(self, max_rounds):
        """Vérifie si le nombre maximum de rounds est atteint"""
        if max_rounds is None:
            return False
        return self.round_count >= max_rounds

    def process_round(self):
        """Traite un round complet"""
        self.round_count += 1
        logging.info(f"Début du round {self.round_count}")
        
        print(Fore.YELLOW + f"\n=== ROUND {self.round_count} ===\n")
        
        try:
            for attacker in self.get_turn_order():
                if not attacker.is_alive():
                    continue
                
                target = self.select_target(attacker)
                if not target:
                    break
                
                logging.info(f"{attacker.name} attaque {target.name}")
                self.process_turn(attacker, target)
                
        except Exception as e:
            logging.error(f"Erreur durant le round {self.round_count}: {str(e)}")
            raise

    def process_turn(self, attacker: Character, target: Character):
        try:
            # Simplifier l'en-tête du tour
            print(Fore.YELLOW + f"\n⚔️ TOUR DE {attacker.name.upper()} ⚔️\n")
            
            # Affichage des stats avec les valeurs effectives (incluant les bonus d'équipement)
            print(Fore.CYAN + f"📊 {attacker.name}: Force: {attacker.strength} | Défense: {attacker.defense}")
            
            # Avantages/Désavantages
            class_modifier = ClassAdvantages.get_damage_modifier(
                attacker.character_class, 
                target.character_class
            )
            
            if class_modifier != 1.0:
                if class_modifier > 1:
                    print(Fore.GREEN + f"↗️ Avantage contre {target.character_class}")
                else:
                    print(Fore.RED + f"↘️ Désavantage contre {target.character_class}")
            
            # Action du combat
            ability = self.try_use_ability(attacker, target)
            if ability:
                self._display_ability_use(attacker, target, ability, class_modifier)
            else:
                self._display_normal_attack(attacker, target, class_modifier)
            
            # Affichage minimal des effets actifs
            if attacker.active_effects:
                effects_str = ", ".join(f"{effect_type.value}: {effects[0].value}" 
                                      for effect_type, effects in attacker.active_effects.items())
                print(Fore.MAGENTA + f"\n🔮 Effets: {effects_str}")
            
            # État après l'action - uniquement les barres de vie
            time.sleep(1.0 / self.game_speed)
            display_combat_status(self.team1, self.team2)
            
        except Exception as e:
            logging.error(f"Erreur durant le tour: {str(e)}")
            raise

    def _display_ability_use(self, attacker: Character, target: Character, ability: Ability, class_modifier: float):
        """Affiche l'utilisation d'une capacité avec détails"""
        print(Fore.CYAN + f"\n✨ {attacker.name} utilise {ability.name}!")
        print(Fore.CYAN + f"   {ability.description}")

        # Dégâts de base selon la force actuelle
        base_damage = self.calculate_base_damage(attacker.strength)
        print(f"  → Force ({attacker.strength}): {base_damage} dégâts de base")

        # Bonus de magie pour les sorts
        if attacker.character_class in ["Mage", "Sorceleur"]:
            magic_bonus = self.calculate_magic_bonus(attacker.magic)
            print(Fore.MAGENTA + f"  → Bonus magique ({attacker.magic}): +{magic_bonus} dégâts")
            base_damage += magic_bonus

        # Bonus de classe
        if class_modifier != 1.0:
            bonus_damage = int(base_damage * class_modifier) - base_damage
            if bonus_damage > 0:
                print(Fore.GREEN + f"  → Avantage de classe (+20%): +{bonus_damage} dégâts")
            else:
                print(Fore.RED + f"  → Désavantage de classe (-20%): {bonus_damage} dégâts")
            base_damage = int(base_damage * class_modifier)

        # Réduction défense
        if target.defense < 5:
            reduction = 0
        elif 5 <= target.defense < 10:
            reduction = 5
        elif 10 <= target.defense < 15:
            reduction = 10
        else:
            reduction = 15
        print(Fore.BLUE + f"  → Défense de {target.name} ({target.defense}): -{reduction} dégâts")

        # Dégâts finaux
        final_damage = max(1, base_damage - reduction)
        print(Fore.YELLOW + f"  → Dégâts finaux: {final_damage}")

        # Application des dégâts
        initial_hp = target.hp
        target.take_damage(final_damage)
        print(f"  → HP de {target.name}: {initial_hp} → {target.hp}")

    def _display_normal_attack(self, attacker: Character, target: Character, class_modifier: float):
        """Affiche une attaque normale avec détails"""
        print(Fore.YELLOW + f"⚔️ Attaque normale")
        
        # Dégâts de base selon la force actuelle
        base_damage = self.calculate_base_damage(attacker.strength)
        print(f"  → Force ({attacker.strength}): {base_damage} dégâts de base")

        # Bonus de classe
        if class_modifier != 1.0:
            bonus_damage = int(base_damage * class_modifier) - base_damage
            if bonus_damage > 0:
                print(Fore.GREEN + f"  → Avantage de classe (+20%): +{bonus_damage} dégâts")
            else:
                print(Fore.RED + f"  → Désavantage de classe (-20%): {bonus_damage} dégâts")
            base_damage = int(base_damage * class_modifier)

        # Réduction défense
        if target.defense < 5:
            reduction = 0
        elif 5 <= target.defense < 10:
            reduction = 5
        elif 10 <= target.defense < 15:
            reduction = 10
        else:
            reduction = 15
        print(Fore.BLUE + f"  → Défense de {target.name} ({target.defense}): -{reduction} dégâts")

        # Dégâts finaux
        final_damage = max(1, base_damage - reduction)
        print(Fore.YELLOW + f"  → Dégâts finaux: {final_damage}")

        # Application des dégâts
        initial_hp = target.hp
        target.take_damage(final_damage)
        print(f"  → HP de {target.name}: {initial_hp} → {target.hp}")

    def try_use_ability(self, attacker: Character, target: Character) -> Optional[Ability]:
        """Tente d'utiliser une capacité spéciale"""
        available_abilities = [
            ability for ability in attacker.abilities 
            if ability.current_cooldown == 0
        ]
        
        for ability in available_abilities:
            if random.random() < ability.base_chance:
                ability.current_cooldown = ability.cooldown
                return ability
        return None

    def update_cooldowns(self, character: Character):
        """Met à jour les cooldowns des capacités"""
        for ability in character.abilities:
            if ability.current_cooldown > 0:
                ability.current_cooldown -= 1

    def apply_ability(self, attacker: Character, target: Character, ability: Ability, class_modifier: float):
        """Applique les effets d'une capacité avec le modificateur de classe"""
        print(Fore.CYAN + f"\n✨ {attacker.name} utilise {ability.name}!")
        
        # Animation selon la classe
        if attacker.character_class == "Mage":
            if any(e.type == EffectType.DAMAGE for e in ability.effects):
                fire_effect()
            else:
                magic_sparkle()
        elif attacker.character_class == "Archer":
            arrow_shot()
        elif attacker.character_class == "Guerrier":
            sword_clash()
        
        print(Fore.CYAN + f"   {ability.description}")
        
        for effect in ability.effects:
            if effect.type == EffectType.DAMAGE:
                modified_value = int(effect.value * class_modifier)
                damage = target.take_damage(modified_value)
                self.stats[attacker.name].damage_dealt += damage
                print(Fore.RED + f"💥 {target.name} subit {damage} dégâts!")
            elif effect.type == EffectType.HEAL:
                healing_effect()
                target.apply_effect(effect)
                print(Fore.GREEN + f"💚 {target.name} récupère {effect.value} PV!")
            else:
                attacker.apply_effect(effect)
                effect_name = effect.type.value.replace("_", " ").title()
                print(Fore.GREEN + f"⚡ {effect_name} appliqué à {attacker.name}!")

    def display_final_results(self):
        """Affiche les résultats finaux du combat"""
        # Si des personnages sont morts, utiliser la logique de survie
        if not all(c.is_alive() for c in self.team1 + self.team2):
            if any(c.is_alive() for c in self.team1) and not any(c.is_alive() for c in self.team2):
                result = "✦ VICTOIRE DE L'ÉQUIPE DES HÉROS ✦"
            elif any(c.is_alive() for c in self.team2) and not any(c.is_alive() for c in self.team1):
                result = "❖ VICTOIRE DE L'ÉQUIPE DES CHALLENGERS ❖"
            else:
                result = "⌛ MATCH NUL ⌛"
        else:
            # Si tout le monde est vivant, comparer les points de vie totaux
            team1_total_hp = sum(char.hp for char in self.team1)
            team2_total_hp = sum(char.hp for char in self.team2)
            team1_total_hp_percent = team1_total_hp / sum(char.max_hp for char in self.team1) * 100
            team2_total_hp_percent = team2_total_hp / sum(char.max_hp for char in self.team2) * 100
            
            # Afficher les totaux pour plus de clarté
            print(f"\nPoints de vie restants :")
            print(f"Équipe des Héros : {int(team1_total_hp)} HP ({team1_total_hp_percent:.1f}%)")
            print(f"Équipe des Challengers : {int(team2_total_hp)} HP ({team2_total_hp_percent:.1f}%)")
            
            # Déterminer le vainqueur
            if team1_total_hp_percent > team2_total_hp_percent:
                result = "✦ VICTOIRE DE L'ÉQUIPE DES HÉROS ✦"
            elif team2_total_hp_percent > team1_total_hp_percent:
                result = "❖ VICTOIRE DE L'ÉQUIPE DES CHALLENGERS ❖"
            else:
                result = "⌛ MATCH NUL ⌛"
        
        # Appeler directement la méthode d'affichage
        self._display_final_results_screen(result)

    def _display_final_results_screen(self, result):
        """Affiche l'écran final des résultats"""
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
                stats.append("║" + center_text(f"❤️ HP: {char.hp}/{char.max_hp} ({health_percent}%)", team_width - 2) + "║")
                stats.append("║" + center_text(health_bar(health_percent, 20), team_width - 2) + "║")
                if i < len(team) - 1:
                    stats.append("║" + "─" * (team_width - 2) + "║")
            
            stats.append("╚" + "═" * (team_width - 2) + "╝")
            return stats
        
        # Création des statistiques pour chaque équipe
        team1_stats = create_team_stats(self.team1, "✦ ÉQUIPE DES HÉROS ✦")
        team2_stats = create_team_stats(self.team2, "❖ ÉQUIPE DES CHALLENGERS ❖")
        
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

    def calculate_damage(self, attacker: Character, target: Character, is_ability: bool = False):
        """Calcule les dégâts sans aléatoire"""
        # Dégâts de base selon la force
        if attacker.strength < 10:
            base_damage = 5
        elif 10 <= attacker.strength < 15:
            base_damage = 10
        elif 15 <= attacker.strength < 20:
            base_damage = 15
        else:
            base_damage = 20

        # Bonus de classe (utiliser ClassAdvantages)
        class_modifier = ClassAdvantages.get_damage_modifier(attacker.character_class, target.character_class)
        base_damage = int(base_damage * class_modifier)

        # Bonus de magie pour les sorts
        if is_ability and attacker.character_class in ["Mage", "Sorceleur"]:
            if attacker.magic < 5:
                magic_bonus = 3
            elif 5 <= attacker.magic < 10:
                magic_bonus = 6
            else:
                magic_bonus = 10
            base_damage += magic_bonus

        # Réduction des dégâts selon la défense
        if target.defense < 5:
            damage_reduction = 0
        elif 5 <= target.defense < 10:
            damage_reduction = 5
        elif 10 <= target.defense < 15:
            damage_reduction = 10
        else:
            damage_reduction = 15

        # Application de la réduction
        final_damage = max(1, base_damage - damage_reduction)
        return final_damage

    def calculate_base_damage(self, strength: int) -> int:
        """Calcule les dégâts de base selon la force effective"""
        # Utiliser la force effective (avec bonus d'équipement)
        if strength < 10:
            return 5
        elif 10 <= strength < 20:
            return 15
        elif 20 <= strength < 30:
            return 20
        else:
            return 25

    def calculate_magic_bonus(self, magic: int) -> int:
        """Calcule le bonus de magie"""
        if magic < 5:
            return 3
        elif 5 <= magic < 15:
            return 8
        elif 15 <= magic < 25:
            return 15
        else:
            return 20

    def process_ability(self, attacker: Character, target: Character, ability: Ability):
        """Traite les effets des capacités spéciales"""
        if ability.name == "Signe de Quen":
            # C'est un bouclier, pas une attaque
            buff_defense = 6
            attacker.apply_buff("defense", buff_defense, 2)
            print(f"  → {attacker.name} gagne {buff_defense} points de défense pour 2 tours")
            return 0
        # ... autres capacités ...

def health_bar(percentage, width=20):
    """Crée une barre de vie visuelle"""
    filled = int(width * percentage / 100)
    bar = "█" * filled + "░" * (width - filled)
    return bar

def display_combat_status(team1: List[Character], team2: List[Character]):
    """Version simplifiée de l'affichage du statut de combat"""
    terminal_width = get_terminal_size()
    team_width = (terminal_width - 4) // 2
    
    # Afficher uniquement les barres de vie
    for i in range(max(len(team1), len(team2))):
        char1 = team1[i] if i < len(team1) else None
        char2 = team2[i] if i < len(team2) else None
        
        if char1:
            hp_percent1 = int((char1.hp / char1.max_hp) * 100)
            health_color1 = (Fore.GREEN if hp_percent1 > 50 
                           else Fore.YELLOW if hp_percent1 > 25 
                           else Fore.RED)
            hp_bar1 = create_compact_health_bar(char1.hp, char1.max_hp)
            print(f"{Fore.CYAN}{char1.name}: {health_color1}{hp_bar1}", end="    ")
        
        if char2:
            hp_percent2 = int((char2.hp / char2.max_hp) * 100)
            health_color2 = (Fore.GREEN if hp_percent2 > 50 
                           else Fore.YELLOW if hp_percent2 > 25 
                           else Fore.RED)
            hp_bar2 = create_compact_health_bar(char2.hp, char2.max_hp)
            print(f"{Fore.RED}{char2.name}: {health_color2}{hp_bar2}")
        elif char1:
            print()  # Nouvelle ligne si seulement char1 existe

def create_compact_health_bar(current_hp, max_hp, bar_length=20):
    """Crée une barre de vie compacte avec des valeurs entières"""
    # Arrondir les HP à l'entier le plus proche
    current_hp = round(current_hp)  # Utilisation de round() au lieu de int()
    percentage = int((current_hp / max_hp) * 100)  # Pourcentage en entier
    filled_length = int(bar_length * current_hp / max_hp)
    
    # Utilisation de caractères plus compacts pour la barre
    bar = '█' * filled_length + '▒' * (bar_length - filled_length)
    
    # Format plus compact pour l'affichage, sans décimales
    return f"[{bar}] {current_hp}/{max_hp} ({percentage}%)"

class CombatStats:
    def __init__(self):
        self.damage_dealt = 0
        self.abilities_used = 0
        self.hits = 0
        self.kills = 0

class ClassAdvantages:
    """Gestion des avantages/désavantages entre classes"""
    
    ADVANTAGES = {
        "Guerrier": ["Archer"],    # Guerrier fort contre Archer
        "Archer": ["Mage"],        # Archer fort contre Mage
        "Mage": ["Guerrier"]       # Mage fort contre Guerrier
    }
    
    @staticmethod
    def get_damage_modifier(attacker_class: str, defender_class: str) -> float:
        """Calcule le modificateur de dégâts basé sur les classes"""
        if defender_class in ClassAdvantages.ADVANTAGES.get(attacker_class, []):
            return 1.2  # 20% de bonus de dégâts
        elif attacker_class in ClassAdvantages.ADVANTAGES.get(defender_class, []):
            return 0.8  # 20% de malus de dégâts
        return 1.0

