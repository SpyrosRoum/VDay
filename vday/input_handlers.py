import pygame


def handle_events(event):
    answer = dict()
    if event.type == pygame.KEYDOWN:
        key = event.key

        if key == pygame.K_ESCAPE:
            # TODO Bring up a menu
            return {'exit': True}
        if key == pygame.K_RETURN:
            if event.mod & pygame.KMOD_ALT:
                return {'fullscreen': True}
    elif event.type == pygame.QUIT:
        return {'exit': True}

    return answer


def handle_keys(pressed_keys):
    if pressed_keys[pygame.K_RIGHT]:
        return {'move': (5, 0)}
    if pressed_keys[pygame.K_LEFT]:
        return {'move': (-5, 0)}
    if pressed_keys[pygame.K_UP]:
        return {'move': (0, -5)}
    if pressed_keys[pygame.K_DOWN]:
        return {'move': (0, 5)}

    return dict()
