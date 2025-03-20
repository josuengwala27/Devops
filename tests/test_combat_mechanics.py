import unittest
from combat import ClassAdvantages, CombatSystem
from characters import Character

class TestCombatMechanics(unittest.TestCase):
    def setUp(self):
        self.guerrier = Character("Guerrier", 5, character_class="Guerrier")
        self.archer = Character("Archer", 6, character_class="Archer")
        self.mage = Character("Mage", 4, character_class="Mage")

    def test_class_advantages(self):
        """Teste les avantages/désavantages entre classes"""
        # Guerrier vs Archer
        mod = ClassAdvantages.get_damage_modifier("Guerrier", "Archer")
        self.assertEqual(mod, 1.2)
        
        # Archer vs Guerrier
        mod = ClassAdvantages.get_damage_modifier("Archer", "Guerrier")
        self.assertEqual(mod, 0.8)
        
        # Classes identiques
        mod = ClassAdvantages.get_damage_modifier("Guerrier", "Guerrier")
        self.assertEqual(mod, 1.0)

    def test_equipment_stats(self):
        """Teste l'impact des équipements sur les stats"""
        from equipment import EQUIPMENT_CATALOG
        
        # Équiper une épée
        self.guerrier.equip(EQUIPMENT_CATALOG["Épée longue"])
        self.assertEqual(self.guerrier.strength, 15)  # Base 10 + 5
        
        # Équiper une armure
        self.guerrier.equip(EQUIPMENT_CATALOG["Armure de plaques"])
        self.assertEqual(self.guerrier.defense, 13)  # Base 5 + 8

    def test_morale_impact(self):
        """Teste l'impact du moral sur les performances"""
        base_strength = self.guerrier.effective_strength
        self.guerrier.update_morale(-50)  # Moral à 50
        self.assertLess(self.guerrier.effective_strength, base_strength)

    def test_fatigue_system(self):
        """Teste le système de fatigue"""
        base_strength = self.guerrier.effective_strength
        self.guerrier.increase_fatigue(50)
        self.assertLess(self.guerrier.effective_strength, base_strength) 