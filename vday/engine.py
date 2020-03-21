import tcod
import tcod.event

from components.fighter import Fighter
from entity import Entity, get_blocking_entity_in
from input_handlers import handle_event
from fov_functions import init_fov, recompute_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import render_all, clear_all

colors = {
    'dark_wall': tcod.Color(0, 0, 100),
    'dark_ground': tcod.Color(50, 50, 150),
    'light_wall': tcod.Color(130, 110, 50),
    'light_ground': tcod.Color(200, 180, 50)
}

class Game:
    def __init__(self):
        self.screen_width = 80
        self.screen_height = 50
        map_width = 80
        map_height = 45

        room_max_size = 10
        room_min_size = 6
        max_rooms = 30

        self.fov_algorithm = 0
        self.fov_light_walls = True
        self.fov_radius = 10

        max_monsters_in_room = 3

        fighter_component = Fighter(hp=30, defense=2, power=5)
        self.player = Entity(0, 0, "@", tcod.white, 'V', blocks=True, fighter=fighter_component)
        self.entities = [self.player]

        tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        self.root = tcod.console_init_root(
            self.screen_width,
            self.screen_height,
            title='VDay',
            fullscreen=False,
            renderer=tcod.RENDERER_SDL2,
            vsync=True,
            order='F'
        )

        self.game_map = GameMap(map_width, map_height)
        self.game_map.make_map(max_rooms, room_min_size, room_max_size, self.player, self.entities, max_monsters_in_room)

        self.fov_map = init_fov(self.game_map)

        self.main_loop()

    def clean_dead(self):
        for entity in filter(lambda ent: ent.fighter is not None, self.entities):
            if entity.fighter.hp <= 0:
                if entity.name != 'V':
                    self.entities.remove(entity)
                else:
                    # TODO handle player death
                    pass

    def main_loop(self):
        fov_recompute = True
        game_state = GameStates.PLAYERS_TURN

        while True:
            for event in tcod.event.get():
                action = handle_event(event)

                if fov_recompute:
                    recompute_fov(self.fov_map, self.player.x, self.player.y, self.fov_radius, self.fov_light_walls, self.fov_algorithm)

                render_all(self.root, self.entities, self.game_map, self.fov_map, fov_recompute, self.screen_width, self.screen_height, colors)

                tcod.console_flush()

                clear_all(self.root, self.entities)

                move = action.get("move")
                exit_ = action.get("exit")
                fullscreen = action.get("fullscreen")

                if move and game_state == GameStates.PLAYERS_TURN:
                    dx, dy = move

                    dest_x = self.player.x + dx
                    dest_y = self.player.y + dy

                    if not self.game_map.is_blocked(dest_x, dest_y):
                        target = get_blocking_entity_in(self.entities, dest_x, dest_y)

                        if target is not None:
                            print(f'You kicked the {target.name}!')
                            death = self.player.fighter.attack(target)
                            if death:
                                self.clean_dead()
                        else:
                            self.player.move(dx, dy)
                            fov_recompute = True

                        game_state = GameStates.ENEMY_TURN

                if exit_:
                    return
                    # self.exit_()

                if fullscreen:
                    tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

                if game_state == GameStates.ENEMY_TURN:
                    for entity in self.entities:
                        if entity.ai:
                            entity.ai.take_turn(self.player, self.fov_map, self.game_map, self.entities)

                    game_state = GameStates.PLAYERS_TURN

        self.exit_()

    def exit_(self):
        # TODO Save?
        pass

if __name__ == "__main__":
    game = Game()
