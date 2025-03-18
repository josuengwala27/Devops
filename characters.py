class Character:
    def __init__(self, name, speed):
        self.name = name
        self.hp = 100
        self.speed = speed

    def is_alive(self):
        return self.hp > 0

    def __repr__(self):
        return f"{self.name} (HP: {self.hp}, Speed: {self.speed})"
