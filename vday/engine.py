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
        tcod.console_flush()


        selected = self.menu()
        # selected = "play"

        if selected == "play":
            self.game_map = GameMap(map_width, map_height)
            self.game_map.make_map(max_rooms, room_min_size, room_max_size, self.player, self.entities, max_monsters_in_room)

            self.fov_map = init_fov(self.game_map)

            self.main_loop()
        elif selected == "exit":
            self.exit_()
        else:
            self.options()

    def clean_dead(self):
        # We only care about entities with fighter comp
        # since the others can't die
        for entity in filter(lambda ent: ent.fighter is not None, self.entities):
            if entity.fighter.hp <= 0:
                if entity.name != 'V':
                    self.entities.remove(entity)
                else:
                    # TODO handle player death
                    pass

    def main_loop(self):
        self.root.clear()

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
                pause = action.get("pause")
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

                if pause:
                    selected = self.options()
                    if selected == "continue":
                        pass
                    elif selected == "exit":
                        self.exit_()

                if exit_:
                    self.exit_()

                if fullscreen:
                    tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

                if game_state == GameStates.ENEMY_TURN:
                    for entity in self.entities:
                        if entity.ai:
                            entity.ai.take_turn(self.player, self.fov_map, self.game_map, self.entities)

                    game_state = GameStates.PLAYERS_TURN

        self.exit_()

    def menu(self, start_screen=True):
        entries = [
            "play",
            "options",
            "exit"
        ]
        cur_index = 0


        while True:
            self.print_entries(entries, cur_index)

            for event in tcod.event.get():
                if event.type == "QUIT":
                    self.exit_()
                if event.type != "KEYDOWN":
                    continue
                if event.repeat:
                    continue
                if event.sym == tcod.event.K_RETURN:
                    return entries[cur_index]

                if event.sym == tcod.event.K_DOWN:
                    if len(entries) - 1 == cur_index:
                        continue
                    cur_index += 1
                    break
                elif event.sym == tcod.event.K_UP:
                    if cur_index == 0:
                        continue
                    cur_index -= 1
                    break
            # TODO highlight curent

    def print_entries(self, entries, cur_index):
        for i, entry in enumerate(entries):
            if i == cur_index:
                fg = tcod.white
                bg = tcod.light_blue
            else:
                fg = tcod.grey
                bg = tcod.black

            self.root.print(
                self.root.width // 2,
                self.root.height // 2 - len(entries) + i,
                entry.title(),
                fg,
                bg,
                alignment=tcod.LEFT
            )

        tcod.console_flush()


    def options(self):
        # TODO the options
        print("We are in options now!")

    def exit_(self):
        # TODO Save?
        raise SystemExit

if __name__ == "__main__":
    game = Game()
