from dataclasses import dataclass
from enum import Enum
from typing import Dict

class EquipmentType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"

class EquipmentSlot(Enum):
    MAIN_HAND = "main_hand"
    OFF_HAND = "off_hand"
    HEAD = "head"
    CHEST = "chest"
    LEGS = "legs"
    RING = "ring"
    AMULET = "amulet"

VALID_STATS = {"strength", "defense", "speed", "hp", "magic"}

@dataclass
class Equipment:
    name: str
    type: EquipmentType
    slot: EquipmentSlot
    stats: Dict[str, int]
    description: str
    
    def __post_init__(self):
        # Validation des stats
        for stat, value in self.stats.items():
            if stat not in VALID_STATS:
                raise ValueError(f"Stat invalide: {stat}")
            if value < -10 or value > 20:  # Limites raisonnables
                raise ValueError(f"Valeur de stat invalide pour {stat}: {value}")

    def __str__(self):
        stats_str = ", ".join(f"{k}: {v}" for k, v in self.stats.items())
        return f"{self.name} ({self.type.value}) [{stats_str}]"

# Définition des sets d'équipement par classe
DEFAULT_CLASS_EQUIPMENT = {
    "Guerrier": {
        "main_hand": "Épée longue",
        "off_hand": "Bouclier en acier",
        "head": "Casque de guerre",
        "chest": "Armure de plaques",
        "legs": "Jambières en acier",
        "ring": "Anneau de force",
        "amulet": "Amulette du guerrier"
    },
    "Archer": {
        "main_hand": "Arc elfique",
        "off_hand": "Carquois en cuir",
        "head": "Capuche de ranger",
        "chest": "Armure de cuir",
        "legs": "Bottes de célérité",
        "ring": "Anneau de précision",
        "amulet": "Amulette du chasseur"
    },
    "Mage": {
        "main_hand": "Bâton magique",
        "off_hand": "Grimoire ancien",
        "head": "Chapeau de mage",
        "chest": "Robe de mage",
        "legs": "Bottes de sagesse",
        "ring": "Anneau de mana",
        "amulet": "Amulette mystique"
    },
    "Sorceleur": {
        "main_hand": "Épée d'argent",
        "off_hand": "Épée d'acier",
        "head": "Médaillon de sorceleur",
        "chest": "Armure de sorceleur",
        "legs": "Bottes de sorceleur",
        "ring": "Anneau de signes",
        "amulet": "Amulette de mutation"
    }
}

# Mise à jour du catalogue d'équipements
EQUIPMENT_CATALOG = {
    # Équipements de Guerrier
    "Épée longue": Equipment(
        name="Épée longue",
        type=EquipmentType.WEAPON,
        slot=EquipmentSlot.MAIN_HAND,
        stats={"strength": 5},
        description="Une épée bien équilibrée"
    ),
    "Bouclier en acier": Equipment(
        name="Bouclier en acier",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.OFF_HAND,
        stats={"defense": 4},
        description="Un solide bouclier en acier"
    ),
    # Équipements d'Archer
    "Arc elfique": Equipment(
        name="Arc elfique",
        type=EquipmentType.WEAPON,
        slot=EquipmentSlot.MAIN_HAND,
        stats={"strength": 4, "speed": 2},
        description="Un arc précis et rapide"
    ),
    "Carquois en cuir": Equipment(
        name="Carquois en cuir",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.OFF_HAND,
        stats={"speed": 1},
        description="Un carquois léger et pratique"
    ),
    # Équipements de Mage
    "Bâton magique": Equipment(
        name="Bâton magique",
        type=EquipmentType.WEAPON,
        slot=EquipmentSlot.MAIN_HAND,
        stats={"strength": 3, "magic": 5},
        description="Amplifie les sorts magiques"
    ),
    "Robe de mage": Equipment(
        name="Robe de mage",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.CHEST,
        stats={"defense": 3, "magic": 3},
        description="Robe enchantée pour mages"
    ),
    "Armure de cuir": Equipment(
        name="Armure de cuir",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.CHEST,
        stats={"defense": 4, "speed": 1},
        description="Armure légère pour archers"
    ),
    # Équipements de Sorceleur
    "Épée d'argent": Equipment(
        name="Épée d'argent",
        type=EquipmentType.WEAPON,
        slot=EquipmentSlot.MAIN_HAND,
        stats={"strength": 4, "speed": 1},
        description="Une épée pour les monstres"
    ),
    "Anneau de vigueur": Equipment(
        name="Anneau de vigueur",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.RING,
        stats={"hp": 15},
        description="Augmente la vitalité"
    ),
    "Amulette de protection": Equipment(
        name="Amulette de protection",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.AMULET,
        stats={"defense": 2, "hp": 10},
        description="Protège son porteur"
    ),
    "Casque de guerre": Equipment(
        name="Casque de guerre",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.HEAD,
        stats={"defense": 3},
        description="Protège la tête"
    ),
    # Équipements de jambes
    "Jambières en acier": Equipment(
        name="Jambières en acier",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.LEGS,
        stats={"defense": 3},
        description="Protection robuste pour les jambes"
    ),
    "Bottes de célérité": Equipment(
        name="Bottes de célérité",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.LEGS,
        stats={"speed": 2},
        description="Bottes légères augmentant l'agilité"
    ),
    "Bottes de sagesse": Equipment(
        name="Bottes de sagesse",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.LEGS,
        stats={"magic": 2},
        description="Bottes enchantées pour mages"
    ),
    "Bottes de sorceleur": Equipment(
        name="Bottes de sorceleur",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.LEGS,
        stats={"speed": 1, "defense": 1},
        description="Bottes renforcées de sorceleur"
    ),
    
    # Équipements de tête manquants
    "Capuche de ranger": Equipment(
        name="Capuche de ranger",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.HEAD,
        stats={"speed": 1, "defense": 1},
        description="Capuche légère de ranger"
    ),
    "Chapeau de mage": Equipment(
        name="Chapeau de mage",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.HEAD,
        stats={"magic": 3},
        description="Chapeau amplifiant la magie"
    ),
    "Médaillon de sorceleur": Equipment(
        name="Médaillon de sorceleur",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.HEAD,
        stats={"magic": 2, "defense": 1},
        description="Médaillon magique de l'école du loup"
    ),
    
    # Anneaux et amulettes spécifiques
    "Anneau de force": Equipment(
        name="Anneau de force",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.RING,
        stats={"strength": 3},
        description="Augmente la force physique"
    ),
    "Anneau de précision": Equipment(
        name="Anneau de précision",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.RING,
        stats={"speed": 2},
        description="Améliore la précision"
    ),
    "Anneau de mana": Equipment(
        name="Anneau de mana",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.RING,
        stats={"magic": 3},
        description="Amplifie la puissance magique"
    ),
    "Anneau de signes": Equipment(
        name="Anneau de signes",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.RING,
        stats={"magic": 2, "strength": 1},
        description="Renforce les signes de sorceleur"
    ),
    "Armure de plaques": Equipment(
        name="Armure de plaques",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.CHEST,
        stats={"defense": 6},
        description="Armure lourde offrant une excellente protection"
    ),
    "Grimoire ancien": Equipment(
        name="Grimoire ancien",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.OFF_HAND,
        stats={"magic": 3},
        description="Un grimoire contenant des sorts anciens"
    ),
    "Épée d'acier": Equipment(
        name="Épée d'acier",
        type=EquipmentType.WEAPON,
        slot=EquipmentSlot.OFF_HAND,
        stats={"strength": 3},
        description="Une épée pour les humains"
    ),
    "Armure de sorceleur": Equipment(
        name="Armure de sorceleur",
        type=EquipmentType.ARMOR,
        slot=EquipmentSlot.CHEST,
        stats={"defense": 4, "speed": 1},
        description="Armure légère mais résistante"
    ),
    "Amulette du guerrier": Equipment(
        name="Amulette du guerrier",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.AMULET,
        stats={"strength": 2, "defense": 2},
        description="Renforce la puissance au combat"
    ),
    "Amulette du chasseur": Equipment(
        name="Amulette du chasseur",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.AMULET,
        stats={"speed": 2, "strength": 1},
        description="Améliore la précision et la vitesse"
    ),
    "Amulette mystique": Equipment(
        name="Amulette mystique",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.AMULET,
        stats={"magic": 4},
        description="Amplifie les pouvoirs magiques"
    ),
    "Amulette de mutation": Equipment(
        name="Amulette de mutation",
        type=EquipmentType.ACCESSORY,
        slot=EquipmentSlot.AMULET,
        stats={"strength": 2, "magic": 2},
        description="Renforce les mutations de sorceleur"
    )
}

# Équipements recommandés par classe
CLASS_EQUIPMENT_SETS = {
    "Guerrier": ["Épée longue", "Armure de plaques", "Casque de guerre"],
    "Mage": ["Bâton magique", "Robe de mage", "Amulette de protection"],
    "Archer": ["Arc elfique", "Armure de cuir", "Anneau de vigueur"]
} 