class Character:
    def __init__(self, name, speed, hp=100):
        self.name = name
        self.speed = speed
        self._hp = hp  # Variable privée avec underscore
        self.max_hp = hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))  # Garantit que HP reste entre 0 et max_hp
        
    def take_damage(self, damage):
        self.hp = self._hp - damage  # Utilise le setter
        
    def is_alive(self):
        return self._hp > 0

    def __str__(self):
        return f"{self.name} (Speed: {self.speed}, HP: {self._hp}/{self.max_hp})"
