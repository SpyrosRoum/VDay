import pygame
import tcod

from map_objects import Tile

class GameMap:
    cell_width = None
    cell_height = None
    tiles = None

    def __init__(self, width, height, cell_width, cell_height):
        self.width = width
        self.height = height

        self.__class__.cell_width = cell_width
        self.__class__.cell_height = cell_height

        self.__class__.tiles = self.create_map()

    def create_map(self):
        return [[Tile("assets/sprites/floor1.jpg", False) for y in range(0, self.height)] for x in range(0, self.width)]

    def init_fov(self):
        self.fov_map = tcod.map.Map(self.width, self.height)

        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[x][y]
                self.fov_map.transparent[x][y] = not tile.block_sight
                # fov_map.walkable[x][y] = not tile.blocked

        return self.fov_map

    def calc_fov(self, x, y):
        self.fov_map.compute_fov(x, y, radius=10)

def draw_map(screen, map_):
    for x in range(0, map_.width):
        for y in range(map_.height):
            tile = map_.tiles[x][y]

            if map_.fov_map.fov[y, x]:
                tile.visited = True
                screen.blit(tile.surf, (x * map_.cell_width, y * map_.cell_height))
            else:
                if tile.visited:
                    surf = tile.surf.copy()
                    surf.fill((40, 50, 60), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(surf, (x * map_.cell_width, y * map_.cell_height))
                else:
                    surf = pygame.Surface((32, 32))
                    surf.fill((48, 27, 44))
                    screen.blit(
                        surf, (x * map_.cell_width, y * map_.cell_height))

