from entity import Entity

class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_dmg(self, from_, amount):
        print(f"{self.owner.name} got {amount} damage from {from_.owner.name}")

        self.hp -= amount

        if self.hp <= 0 and self.owner.name != 'V':
            print(f"The {self.owner.name} died")
        elif self.hp <= 0:
            # TODO: handle player death
            pass

    def attack(self, target: Entity):
        damage = self.power - target.fighter.defense

        if damage < 0:
            damage = 1

        target.fighter.take_dmg(self, damage)
