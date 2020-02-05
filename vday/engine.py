import pygame

from entity import Entity
from input_handlers import handle_events, handle_keys


class Game:

    def __init__(self):
        pygame.init()

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
            all_ = Entity.get("all")
            all_.draw(self.screen)
            # self.screen.blit(self.player.surf, self.player.rect)

            pygame.display.flip()

        self.clean_up()


    def clean_up(self):
        pygame.quit()


if __name__ == "__main__":
    game = Game()
