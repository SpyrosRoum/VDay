from pygame import sprite
import pygame


class Tile(sprite.Sprite):
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, path, blocked, block_sight=None):
        self.blocked = blocked
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

        self.surf = pygame.image.load(path).convert()
        self.rect = self.surf.get_rect()

        self.visited = False

