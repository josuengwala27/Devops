import unittest
from characters import Character, Effect, EffectType
from combat import CombatSystem, ClassAdvantages

class TestCombat(unittest.TestCase):
    def setUp(self):
        """Initialise le système de combat pour chaque test"""
        self.team1 = [
            Character("Hero", 5, character_class="Guerrier"),
            Character("Mage", 4, character_class="Mage")
        ]
        self.team2 = [
            Character("Enemy", 5, character_class="Archer"),
            Character("Boss", 6, character_class="Guerrier")
        ]
        self.combat = CombatSystem(self.team1, self.team2)

    def test_combat_initialization(self):
        """Teste l'initialisation du combat"""
        self.assertEqual(len(self.combat.team1), 2)
        self.assertEqual(len(self.combat.team2), 2)
        self.assertEqual(len(self.combat.stats), 4)

    def test_ability_usage(self):
        """Teste l'utilisation des capacités"""
        attacker = self.team1[0]
        target = self.team2[0]
        ability = self.combat.try_use_ability(attacker, target)
        if ability:  # Car c'est aléatoire
            self.assertIn(ability, attacker.abilities)

    def test_combat_stats(self):
        """Teste le système de statistiques de combat"""
        attacker = self.team1[0]
        target = self.team2[0]
        
        # Simuler une attaque
        self.combat.process_turn(attacker, target)
        
        # Vérifier que les stats sont mises à jour
        stats = self.combat.stats[attacker.name]
        self.assertGreaterEqual(stats.damage_dealt, 0)

    def test_dot_effect(self):
        """Teste les dégâts sur la durée"""
        attacker = self.team1[0]
        target = self.team2[0]
        initial_hp = target.hp
        
        effect = Effect(EffectType.DOT, 5, 3)
        target.apply_effect(effect)
        
        for _ in range(3):
            target.update_effects()
            
        self.assertEqual(target.hp, initial_hp - 15)  # 5 dégâts * 3 tours

    def test_class_advantages_full(self):
        """Teste tous les avantages/désavantages de classe"""
        for attacker_class in ["Guerrier", "Archer", "Mage"]:
            for defender_class in ["Guerrier", "Archer", "Mage"]:
                modifier = ClassAdvantages.get_damage_modifier(
                    attacker_class, defender_class
                )
                if defender_class in ClassAdvantages.ADVANTAGES[attacker_class]:
                    self.assertEqual(modifier, 1.2)
                elif attacker_class in ClassAdvantages.ADVANTAGES[defender_class]:
                    self.assertEqual(modifier, 0.8)
                else:
                    self.assertEqual(modifier, 1.0)

    def test_display_final_results(self):
        """Teste l'affichage des résultats finaux"""
        # Simuler la mort de tous les personnages de l'équipe 2
        for character in self.team2:
            character._hp = 0
        
        self.combat.display_final_results()
        # Vérifier que les stats sont bien mises à jour
        for char_name, stats in self.combat.stats.items():
            self.assertIsNotNone(stats) 