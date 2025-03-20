import unittest
from characters import Character, Effect, EffectType, Ability
from equipment import Equipment, EquipmentSlot, EquipmentType

class TestCharacter(unittest.TestCase):
    def setUp(self):
        """Initialise un personnage pour chaque test"""
        self.character = Character(
            name="Test Warrior",
            speed=5,
            strength=10,
            defense=5,
            hp=100,
            character_class="Guerrier"
        )

    def test_character_creation(self):
        """Teste la création basique d'un personnage"""
        self.assertEqual(self.character.name, "Test Warrior")
        self.assertEqual(self.character.speed, 5)
        self.assertEqual(self.character.strength, 10)
        self.assertEqual(self.character.defense, 5)
        self.assertEqual(self.character.hp, 100)
        self.assertEqual(self.character.character_class, "Guerrier")

    def test_take_damage(self):
        """Teste le système de dégâts"""
        damage_taken = self.character.take_damage(10)
        self.assertEqual(damage_taken, 5)  # 10 - 5 (defense)
        self.assertEqual(self.character.hp, 95)

    def test_equipment_stats(self):
        """Teste l'impact de l'équipement sur les stats"""
        sword = Equipment(
            name="Test Sword",
            type=EquipmentType.WEAPON,
            slot=EquipmentSlot.MAIN_HAND,
            stats={"strength": 5},
            description="Test weapon"
        )
        self.character.equip(sword)
        self.assertEqual(self.character.strength, 15)  # base 10 + 5

    def test_abilities(self):
        """Teste les capacités du personnage"""
        abilities = self.character.abilities
        self.assertTrue(any(a.name == "Coup Puissant" for a in abilities))
        self.assertTrue(any(a.name == "Cri de Guerre" for a in abilities))

    def test_morale_system(self):
        """Teste le système de moral"""
        self.character.update_morale(-20)
        self.assertEqual(self.character.morale, 80)
        self.assertLess(self.character.combat_modifier, 1)

    def test_fatigue_system(self):
        """Teste le système de fatigue"""
        self.character.increase_fatigue(30)
        self.assertEqual(self.character.fatigue, 30)
        self.assertLess(self.character.combat_modifier, 1)

    def test_effect_application(self):
        """Teste l'application des effets"""
        effect = Effect(EffectType.BUFF_STRENGTH, 5, 2)
        self.character.apply_effect(effect)
        self.assertEqual(self.character.strength, 15)  # base 10 + 5

    def test_negative_stats(self):
        """Teste la gestion des stats négatives"""
        char = Character("Test", speed=-1, strength=-5, defense=-3)
        self.assertGreaterEqual(char.speed, 1)
        self.assertGreaterEqual(char.strength, 1)
        self.assertGreaterEqual(char.defense, 0)

    def test_invalid_equipment(self):
        """Teste la gestion des équipements invalides"""
        with self.assertRaises(TypeError):
            self.character.equip("Not an equipment") 