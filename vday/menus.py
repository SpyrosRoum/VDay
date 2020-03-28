from typing import Iterable, Optional

import tcod


class Menu(tcod.event.EventDispatch):
    def __init__(self, entries: Iterable[str], root: tcod.console.Console, name: Optional[str] = ""):
        self.entries = entries
        self.selected_entry = None

        self.console = tcod.console.Console(
            root.width // 4,
            root.height // 4,
        )

        self.console.draw_frame(
            0,
            0,
            self.console.width,
            self.console.height,
            name,
            False,
            fg=tcod.white,
            bg=tcod.black
        )

        self.current_entry = 0
        self.print_entries()

    def print_entries(self):
        for i, entrie in enumerate(self.entries):
            if i == self.current_entry:
                fg = tcod.white
                bg = tcod.light_blue
            else:
                fg = tcod.grey
                bg = tcod.black

            self.console.print(
                self.console.width//2-5,
                self.console.height//2-3+i,
                entrie.title(),
                fg,
                bg,
                alignment=tcod.LEFT,
            )

        tcod.console_flush()

    def ev_keydown(self, event):
        if event.repeat:
            return

        if event.sym == tcod.event.K_DOWN:
            self.updated = True
            if self.current_entry < len(self.entries) - 1:
                self.current_entry += 1
        elif event.sym == tcod.event.K_UP:
            self.updated = True
            if self.current_entry > 0:
                self.current_entry -= 1
        elif event.sym == tcod.event.K_RETURN:
            self.selected_entry = {self.entries[self.current_entry]: True}
            return

        self.print_entries()

    def ev_quit(self, event):
        self.selected_entry = {'end': True}

