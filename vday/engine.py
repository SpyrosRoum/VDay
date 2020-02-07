import pygame

from entity import Entity
from input_handlers import handle_events, handle_keys
from map_objects import GameMap, draw_map


class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.fps = 30
        self.width = 800
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("VDay")


        self.map = GameMap(30, 30, 32, 32)
        self.fov_map = self.map.init_fov()

        self.player = Entity("Player", type_="player", path="assets/sprites/player.png", x=0 * self.map.cell_width, y=0 * self.map.cell_height)

        self.main_loop()

    def main_loop(self):
        running = True
        calc_fov = True

        while running:
            # Look through all the events in the q
            for event in pygame.event.get():
                answer = handle_events(event)
                if answer == dict():
                    break

                if answer.get("exit"):
                    running = False
                if answer.get("fullscreen"):
                    # TODO Make it toggle fullscreen
                    # Seems to be weird in pygame
                    pass

            pressed_keys = pygame.key.get_pressed()
            answer = handle_keys(pressed_keys)
            if direction := answer.get("move"):
                calc_fov = True
                self.player.move(self.map, *direction)

            self.screen.fill((255, 255, 255))
            if calc_fov:
                self.map.calc_fov(self.player.x, self.player.y)
            draw_map(self.screen, self.map)

            # Print all entites
            # TODO print only visible entities?
            all_ = Entity.get("all")
            for entity in all_:
                entity.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)
            calc_fov = False


        self.clean_up()


    def clean_up(self):
        # TODO maybe save current state of the game
        pygame.quit()


if __name__ == "__main__":
    game = Game()
