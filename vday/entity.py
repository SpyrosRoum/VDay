import pygame
from pygame import sprite


class Entity(sprite.Sprite):
    entities = sprite.Group()
    enemies = sprite.Group()
    items = sprite.Group()
    friends = sprite.Group()

    def __init__(self, name, type_, path=None, ai=None, fighter=None):
        super(Entity, self).__init__()

        self.name = name
        self.type_ = type_

        if path is not None:
            self.surf = pygame.image.load(path).convert_alpha()
            # self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
            self.rect = self.surf.get_rect()
        else:
            self.surf = pygame.Surface((50, 25))
            self.surf.fill((255, 255, 255))
            self.rect = self.surf.get_rect()

        self.__class__.add_to_groups(self)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

        if self.type_ == "player":
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

    def update(self):
        if self.ai is not None:
            self.ai.update()

    @classmethod
    def add_to_groups(cls, entity):
        cls.entities.add(entity)

        if entity.type_ == "enemy":
            cls.enemies.add(entity)
        if entity.type_ == "item":
            cls.items.add(entity)
        if entity.type_ == "friend":
            cls.friends.add(entity)

    @classmethod
    def get(cls, type_):
        return {
            "all": cls.entities,
            "enemies": cls.enemies,
            "items": cls.items,
            "friends": cls.friends,
        }[type_]
