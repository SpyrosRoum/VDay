import tcod

from components.fighter import Fighter
from entity import Entity, get_blocking_entity_in
from input_handlers import handle_keys
from fov_functions import init_fov, recompute_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import render_all, clear_all

def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_in_room = 3

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, "@", tcod.white, 'Player', blocks=True, fighter=fighter_component)
    entities = [player]

    tcod.console_set_custom_font('vday/arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    root = tcod.console_init_root(
        screen_width,
        screen_height,
        title='VDay',
        fullscreen=False,
        renderer=tcod.RENDERER_SDL2,
        vsync=True,
        order='F'
    )

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, player, entities, max_monsters_in_room)

    fov_recompute = True

    fov_map = init_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(root, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        tcod.console_flush()

        clear_all(root, entities)

        action = handle_keys(key)

        move = action.get("move")
        exit_ = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move

            dest_x = player.x + dx
            dest_y = player.y + dy

            if not game_map.is_blocked(dest_x, dest_y):
                target = get_blocking_entity_in(entities, dest_x, dest_y)

                if target is not None:
                    print(f'You kicked the {target.name}!')
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit_:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    entity.ai.take_turn(player, fov_map, game_map, entities)

            game_state = GameStates.PLAYERS_TURN

if __name__ == "__main__":
    main()
