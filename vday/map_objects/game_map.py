import pygame
from map_objects import Tile

class GameMap:
    def __init__(self, width, height, cell_width, cell_height):
        self.width = width
        self.height = height

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.tiles = self.create_map()


    def create_map(self):
        return [[Tile("assets/sprites/floor1.jpg", False) for y in range(0, self.height)] for x in range(0, self.width)]

def draw_map(screen, map_):
    for x in range(0, map_.width):
        for y in range(map_.height):
            tile = map_.tiles[x][y]
            if tile.visited:
                screen.blit(tile.surf, (x * map_.cell_width, y * map_.cell_height))
            else:
                surf = pygame.Surface((32, 32))
                surf.fill((48, 27, 44))
                screen.blit(surf, (x * map_.cell_width, y * map_.cell_height))
