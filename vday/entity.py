import pygame
from pygame import sprite

class Entity(sprite.Sprite):
    def __init__(self, player=False):
        super(Entity, self).__init__()

        self.player = player
        self.surf = pygame.Surface((50, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

        if self.player:
            # Keep him visible
            # width, height = pygame.display.get_window_size() # New in pygame v2
            info = pygame.display.Info()
            width = info.current_w
            height = info.current_h

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > width:
                self.rect.right = width
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= height:
                self.rect.bottom = height
