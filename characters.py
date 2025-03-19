class Character:
    def __init__(self, name, speed, strength=10, defense=5, hp=100, character_class="Guerrier"):
        self.name = name
        self.speed = speed
        self.strength = strength
        self.defense = defense
        self._hp = hp
        self.max_hp = hp
        self.character_class = character_class

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))
        
    def take_damage(self, damage):
        # Prise en compte de la défense dans les dégâts
        actual_damage = max(0, damage - self.defense)
        self.hp = self._hp - actual_damage
        return actual_damage
        
    def is_alive(self):
        return self._hp > 0

    def __str__(self):
        return f"{self.name} [{self.character_class}] (Speed: {self.speed}, STR: {self.strength}, DEF: {self.defense}, HP: {self._hp}/{self.max_hp})"
