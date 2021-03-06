import math

class Entity:
    """
    A generic object to represent players, enemies, items, etc
    """
    def __init__(self, x, y, char, color, name, blocks=False, **kwargs): # friend=False, friend_strength=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

        self.fighter = kwargs.get('fighter')
        self.ai = kwargs.get('ai')

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        # Move the entity by a giver amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx **2 + dy ** 2)

        dx = round(dx / distance)
        dy = round(dy / distance)

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entity_in(entities, self.x + dx, self.y + dy)):
                self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)


def get_blocking_entity_in(entities, x, y):
    for entity in entities:
        if entity.x == x and entity.y == y and entity.blocks:
            return entity

    return None
