from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict
from equipment import Equipment, EquipmentSlot, EQUIPMENT_CATALOG, DEFAULT_CLASS_EQUIPMENT
from colorama import Fore
import logging

class EffectType(Enum):
    DAMAGE = "damage"
    HEAL = "heal"
    BUFF_STRENGTH = "buff_strength"
    BUFF_DEFENSE = "buff_defense"
    DEBUFF_DEFENSE = "debuff_defense"
    DOT = "damage_over_time"  # Dégâts sur la durée

@dataclass
class Effect:
    type: EffectType
    value: int
    duration: int = 1  # Nombre de tours
    
@dataclass
class Ability:
    name: str
    effects: List[Effect]
    cooldown: int
    description: str
    base_chance: float = 0.3  # 30% de chance d'utilisation par défaut
    current_cooldown: int = 0

class Character:
    # Liste des classes autorisées
    VALID_CLASSES = ["Guerrier", "Archer", "Mage", "Sorceleur"]
    
    def __init__(self, name: str, speed: int, strength: int = 10, 
                 defense: int = 5, hp: int = 100, character_class: str = "Guerrier"):
        if not name or not isinstance(name, str):
            raise ValueError("Le nom doit être une chaîne non vide")
            
        if character_class not in self.VALID_CLASSES:  # Utilisation de VALID_CLASSES
            raise ValueError(f"Classe de personnage invalide. Classes autorisées: {', '.join(self.VALID_CLASSES)}")
            
        self.name = name
        self._base_speed = max(1, speed)
        self._base_strength = max(1, strength)
        self._base_defense = max(0, defense)
        self._base_magic = 0
        
        # Stats effectives (incluant les bonus d'équipement)
        self._speed = self._base_speed
        self._strength = self._base_strength
        self._defense = self._base_defense
        self._magic = self._base_magic
        
        self.max_hp = max(1, hp)
        self._hp = max(1, hp)
        self.character_class = character_class
        self.abilities = self._init_abilities()
        self.active_effects = {}
        self.equipment = {slot: None for slot in EquipmentSlot}
        self.morale = 100
        self.fatigue = 0
        
        # Équiper l'équipement par défaut
        if character_class in DEFAULT_CLASS_EQUIPMENT:
            for slot, item_name in DEFAULT_CLASS_EQUIPMENT[character_class].items():
                if item_name in EQUIPMENT_CATALOG:
                    self.equip(EQUIPMENT_CATALOG[item_name])

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))
        
    def take_damage(self, damage):
        """Calcule et applique les dégâts en tenant compte de la défense"""
        # La défense réduit les dégâts de 5% par point
        damage_reduction = self._defense * 0.05
        # Les dégâts ne peuvent pas être réduits de plus de 80%
        damage_reduction = min(0.8, damage_reduction)
        
        actual_damage = max(1, int(damage * (1 - damage_reduction)))
        self.hp = self._hp - actual_damage
        return actual_damage
        
    def is_alive(self):
        return self._hp > 0

    def __str__(self):
        return f"{self.name} [{self.character_class}] (Speed: {self._speed}, STR: {self._strength}, DEF: {self._defense}, HP: {self._hp}/{self.max_hp})"

    def _init_abilities(self) -> List[Ability]:
        """Initialise les capacités spéciales selon la classe"""
        if self.character_class == "Guerrier":
            return [
                Ability(
                    name="Coup Puissant",
                    effects=[Effect(EffectType.DAMAGE, 20)],
                    cooldown=3,
                    description="Frappe puissante ignorant la défense"
                ),
                Ability(
                    name="Cri de Guerre",
                    effects=[
                        Effect(EffectType.BUFF_STRENGTH, 5, 2),
                        Effect(EffectType.BUFF_DEFENSE, 3, 2)
                    ],
                    cooldown=4,
                    description="Augmente la force et la défense pendant 2 tours"
                )
            ]
        elif self.character_class == "Mage":
            return [
                Ability(
                    name="Boule de Feu",
                    effects=[
                        Effect(EffectType.DAMAGE, 15),
                        Effect(EffectType.DOT, 5, 3)
                    ],
                    cooldown=3,
                    description="Lance une boule de feu qui brûle l'ennemi"
                ),
                Ability(
                    name="Barrière Magique",
                    effects=[Effect(EffectType.BUFF_DEFENSE, 8, 2)],
                    cooldown=4,
                    description="Crée une barrière protectrice"
                )
            ]
        elif self.character_class == "Archer":
            return [
                Ability(
                    name="Tir Précis",
                    effects=[Effect(EffectType.DAMAGE, 25)],
                    cooldown=4,
                    description="Tir puissant ignorant une partie de la défense"
                ),
                Ability(
                    name="Pluie de Flèches",
                    effects=[Effect(EffectType.DAMAGE, 12)],
                    cooldown=3,
                    description="Attaque tous les ennemis"
                )
            ]
        elif self.character_class == "Sorceleur":  # Ajout des capacités du Sorceleur
            return [
                Ability(
                    name="Signe d'Aard",
                    effects=[Effect(EffectType.DAMAGE, 18)],
                    cooldown=3,
                    description="Une vague de force télékinétique"
                ),
                Ability(
                    name="Signe de Quen",
                    effects=[Effect(EffectType.BUFF_DEFENSE, 6, 2)],
                    cooldown=4,
                    description="Un bouclier magique protecteur"
                )
            ]
        return []

    def apply_effect(self, effect: Effect):
        """Applique un effet au personnage"""
        try:
            if effect.type == EffectType.DAMAGE:
                self.take_damage(effect.value)
            elif effect.type == EffectType.HEAL:
                self.hp = min(self.max_hp, self.hp + effect.value)
            elif effect.type in [EffectType.BUFF_STRENGTH, EffectType.BUFF_DEFENSE]:
                if effect.duration > 1:
                    self.active_effects.setdefault(effect.type, []).append(effect)
                if effect.type == EffectType.BUFF_STRENGTH:
                    self._strength += effect.value
                else:
                    self._defense += effect.value
        except Exception as e:
            logging.error(f"Erreur lors de l'application de l'effet {effect.type}: {str(e)}")
            raise
        
    def update_effects(self):
        """Met à jour les effets actifs à la fin du tour"""
        for effect_type, effects in list(self.active_effects.items()):
            for effect in effects[:]:
                effect.duration -= 1
                if effect.type == EffectType.DOT:
                    self.take_damage(effect.value)
                    
                if effect.duration <= 0:
                    if effect_type == EffectType.BUFF_STRENGTH:
                        self._strength -= effect.value
                    elif effect_type == EffectType.BUFF_DEFENSE:
                        self._defense -= effect.value
                    effects.remove(effect)
            if not effects:
                del self.active_effects[effect_type]

    @property
    def speed(self):
        """Calcule la vitesse totale avec les bonus d'équipement"""
        total = self._speed
        for equipment in self.equipment.values():
            if equipment:
                total += equipment.stats.get("speed", 0)
        return max(1, total)  # Toujours minimum 1

    @property
    def strength(self):
        return self._strength

    @property
    def defense(self):
        return self._defense

    @property
    def magic(self):
        return self._magic

    def update_stats_from_equipment(self):
        """Met à jour toutes les stats basées sur l'équipement"""
        self._speed = self._base_speed
        self._strength = self._base_strength
        self._defense = self._base_defense
        self._magic = self._base_magic
        
        for equipment in self.equipment.values():
            if equipment:
                self._speed += equipment.stats.get("speed", 0)
                self._strength += equipment.stats.get("strength", 0)
                self._defense += equipment.stats.get("defense", 0)
                self._magic += equipment.stats.get("magic", 0)

    def equip(self, equipment: Equipment) -> bool:
        """Équipe un objet dans son emplacement"""
        try:
            if not isinstance(equipment, Equipment):
                raise TypeError("L'objet doit être de type Equipment")
                
            if equipment.slot not in self.equipment:
                raise ValueError(f"Emplacement d'équipement invalide: {equipment.slot}")
                
            if self.equipment[equipment.slot]:
                self.unequip(equipment.slot)
                
            self.equipment[equipment.slot] = equipment
            # Mise à jour des stats avec les bonus d'équipement
            for stat, value in equipment.stats.items():
                if stat == "speed":
                    self._speed += value
                elif stat == "strength":
                    self._strength += value
                elif stat == "defense":
                    self._defense += value
                elif stat == "magic":
                    self._magic += value
            return True
            
        except Exception as e:
            print(Fore.RED + f"Erreur d'équipement: {str(e)}")
            return False
        
    def unequip(self, slot: EquipmentSlot) -> Optional[Equipment]:
        """Déséquipe un objet et le retourne"""
        item = self.equipment[slot]
        self.equipment[slot] = None
        # Mise à jour des stats avec les bonus d'équipement
        for stat, value in item.stats.items():
            if stat == "speed":
                self._speed -= value
            elif stat == "strength":
                self._strength -= value
            elif stat == "defense":
                self._defense -= value
            elif stat == "magic":
                self._magic -= value
        return item

    def update_morale(self, value: int):
        """Met à jour le moral du personnage"""
        self.morale = max(0, min(100, self.morale + value))
        
    def increase_fatigue(self, value: int = 5):
        """Augmente la fatigue du personnage"""
        self.fatigue = min(100, self.fatigue + value)
        
    @property
    def combat_modifier(self) -> float:
        """Calcule le modificateur de combat basé sur le moral et la fatigue"""
        morale_mod = (self.morale - 50) / 100  # -0.5 à +0.5
        fatigue_mod = -self.fatigue / 200  # -0.5 à 0
        return 1 + morale_mod + fatigue_mod
        
    @property
    def effective_strength(self) -> int:
        """Force effective tenant compte du moral et de la fatigue"""
        return int(self._strength * self.combat_modifier)
        
    @property
    def effective_defense(self) -> int:
        """Défense effective tenant compte du moral et de la fatigue"""
        return int(self._defense * self.combat_modifier)

    def _equip_default_equipment(self):
        """Équipe l'équipement par défaut selon la classe du personnage"""
        if self.character_class in DEFAULT_CLASS_EQUIPMENT:
            default_equipment = DEFAULT_CLASS_EQUIPMENT[self.character_class]
            for slot, item_name in default_equipment.items():
                if item_name in EQUIPMENT_CATALOG:
                    self.equip(EQUIPMENT_CATALOG[item_name])

    @property
    def base_speed(self):
        return self._base_speed
        
    @property
    def base_strength(self):
        return self._base_strength
        
    @property
    def base_defense(self):
        return self._base_defense
        
    @property
    def base_magic(self):
        return self._base_magic
