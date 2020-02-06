import pygame

from entity import Entity
from input_handlers import handle_events, handle_keys


class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.fps = 30
        self.width = 800
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("VDay")

        self.player = Entity("Player", type_="player", path="assets/sprites/player.png")

        self.main_loop()

    def main_loop(self):
        running = True

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
                self.player.move(*direction)

            self.screen.fill((255, 255, 255))

            # Print all entites
            # TODO print only visible entities?
            all_ = Entity.get("all")
            all_.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)

        self.clean_up()


    def clean_up(self):
        # TODO maybe save current state of the game
        pygame.quit()


if __name__ == "__main__":
    game = Game()
