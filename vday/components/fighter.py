from entity import Entity

class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

        # This gets set where you initialise it
        self.owner: Entity

    def take_dmg(self, from_, amount: int):
        print(f"{self.owner.name} got {amount} damage from {from_.owner.name}")

        self.hp -= amount

        if self.hp <= 0:
            if self.owner.name != 'V':
                print(f"The {self.owner.name} died")
            else:
                print(f"You died by the {from_.owner.name}")

            return True

        return False

    def attack(self, target: Entity):
        damage = self.power - target.fighter.defense

        damage = damage if damage > 0 else 1

        return target.fighter.take_dmg(self, damage)
