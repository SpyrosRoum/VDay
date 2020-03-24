import tcod

def handle_keys(event):
    sym = event.sym

    #* Movement keys
    if sym in [tcod.event.K_UP, tcod.event.K_w]:
        return {'move': (0, -1)}
    if sym in [tcod.event.K_LEFT, tcod.event.K_a]:
        return {'move': (-1, 0)}
    if sym in [tcod.event.K_DOWN, tcod.event.K_s]:
        return {'move': (0, 1)}
    if sym in [tcod.event.K_RIGHT, tcod.event.K_d]:
        return {'move': (1, 0)}

    #* Toggle full screen
    if (event.mod & tcod.event.KMOD_LALT) and sym == tcod.event.K_RETURN:
        return {'fullscreen': True}

    #* Exit
    if sym == tcod.event.K_ESCAPE:
        return {'pause': True}

    #* No key was pressed
    return {}

def handle_event(event):
    if event.type == "KEYDOWN":
        if event.repeat:
            return {}

        return handle_keys(event)

    if event.type == "QUIT":
        return {'exit': True}

    return {}
