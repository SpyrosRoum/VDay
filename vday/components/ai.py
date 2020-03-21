import tcod

from entity import Entity

class BasicMonster:
    def __init__(self):
        self.owner: Entity

    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner

        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)
            else:
                monster.fighter.attack(target)
