import random

import tcod

from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = self.init_tiles()

    def init_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)]
                 for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, player, entities, max_monsters_in_room):
        rooms = []
        num_rooms = 0

        for _ in range(max_rooms):
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)

            x = random.randint(0, self.width - w - 1)
            y = random.randint(0, self.height - h - 1)

            new_room = Rect(x, y, w, h)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                new_x, new_y = new_room.center

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    prev_x, prev_y = rooms[-1].center

                    # flip a coin
                    if random.choice([1, 0]):
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters_in_room)
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_in_room):
        numb_of_monsters = random.randint(0, max_monsters_in_room)

        for _ in range(numb_of_monsters):
            # Choose a random location in the room
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if random.randint(0, 100) < 80:
                    fighter_comp = Fighter(hp=10, defense=0, power=3)
                    ai_comp = BasicMonster()

                    monster = Entity(
                        x,
                        y,
                        'O',
                        tcod.desaturated_green,
                        'Orc',
                        blocks=True,
                        fighter=fighter_comp,
                        ai=ai_comp
                    )
                else:
                    fighter_comp = Fighter(hp=16, defense=1, power=4)
                    ai_comp = BasicMonster()

                    monster = Entity(
                        x,
                        y,
                        'T',
                        tcod.darker_green,
                        'Troll',
                        blocks=True,
                        fighter=fighter_comp,
                        ai=ai_comp
                    )

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
