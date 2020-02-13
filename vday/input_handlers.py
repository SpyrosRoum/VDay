import tcod

def handle_keys(key):
    key_char = chr(key.c)

    #* Movement keys
    if key.vk == tcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    if key.vk == tcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    if key.vk == tcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    if key.vk == tcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    if key_char == 'y':
        return {'move': (-1, -1)}
    if key_char == 'u':
        return {'move': (1, -1)}
    if key_char == 'b':
        return {'move': (-1, 1)}
    if key_char == 'n':
        return {'move': (1, 1)}

    #* Toggle full screen
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    #* Exit
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    #* No key was pressed
    return {}
