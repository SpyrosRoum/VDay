import pygame
from pygame import sprite

from map_objects import GameMap

class Entity(sprite.Sprite):
    entities = sprite.Group()
    enemies = sprite.Group()
    items = sprite.Group()
    friends = sprite.Group()

    def __init__(self, name, type_, path, x, y, ai=None, fighter=None):
        super(Entity, self).__init__()

        self.name = name
        self.type_ = type_
        # Map x, y. Not pixels
        self.x = x
        self.y = y

        self.image = pygame.image.load(path).convert_alpha()
        # self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.image.get_rect()


        self.__class__.add_to_groups(self)

    def move(self, map_, dx, dy):
        if map_.tiles[self.x + dx][self.y + dy].blocked:
            return

        self.x += dx
        self.y += dy


    def update(self):
        if self.ai is not None:
            self.ai.update()

    def draw(self, screen):
        screen.blit(self.image, (self.x * GameMap.cell_width, self.y * GameMap.cell_height))

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
