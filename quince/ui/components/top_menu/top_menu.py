"""
This module contains the class for the top menu, which is where the user can
select a user name, avatar, and control other parameters before starting
a new game.

The TopMenu class requires a root widget when it is instantiated, therefore
it cannot be passed to the main GameApp directly. Instead, a TopMenuFactory
is provided which can be used by the GameApp to instantiate a TopMenu
at runtime.
"""

import tkinter as tk
import os as os
from PIL import Image, ImageTk
from quince.components import Player, NPC
from quince.ui.components.game_frame_factory import GameFrameFactory
from quince.ui.components.top_menu.validating_entry import UserNameEntry

class TopMenu(tk.Frame):
    """Initial frame shown on the main window when
    the app launches. Allows the user to select
    an avatar name and image before starting a new game.
    """
    def __init__(self, root, start_game):
        tk.Frame.__init__(self, root)

        # Callback to the main app that instructs it to hide this menu
        # and show the new game.
        self.start_game = start_game

        self.grid_rowconfigure(0, weight=1) # header pad
        self.grid_rowconfigure(1, weight=0) # avatar + username label
        self.grid_rowconfigure(2, weight=0) # avatar + username entry
        self.grid_rowconfigure(3, weight=0) # avatar label
        self.grid_rowconfigure(4, weight=0) # start game btn
        self.grid_rowconfigure(5, weight=1) # footer pad
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        self.avatar = tk.Label(self, text= "")
        self._display_avatar("quince/ui/assets/avatars/avatar01.png")
        avatar_label = tk.Label(self, text="Click to edit", font=("Helvetica", 8))
        avatar_label.grid(row=3, column=1)

        name_entry_label = tk.Label(self, text="Player Name:")
        name_entry_label.grid(row=1, column=2)
        self.name_entry = UserNameEntry(self, value="Alice", justify="center", char_limit=12)
        self.name_entry.grid(row=2, column=2)

        btn = tk.Button(self, text="New Game", command=self._start_game)
        btn.grid(row=4, column=1, columnspan=2, pady=64)

    def _display_avatar(self, path):
        p = os.path.join(os.getcwd(), path)
        image = Image.open(p)
        image.thumbnail((65, 65), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        self.avatar.destroy()
        self.avatar = tk.Label(self, image=img, cursor="hand2", highlightbackground="black", highlightthickness=1)
        self.avatar.image = img
        self.avatar.grid(row=1, column=1, padx=32, rowspan=2)
        self.avatar.bind("<Enter>", self.on_avatar_enter)
        self.avatar.bind("<Leave>", self.on_avatar_leave)

    def on_avatar_enter(self, e):
        self.avatar.config(highlightbackground="firebrick3")

    def on_avatar_leave(self, e):
        self.avatar.config(highlightbackground="black")

    def _start_game(self):
        """Wraps the callback function provided by the parent GameApp widget.
        Provides the parent with a list of players which it can use to
        initiate a new game.
        """

        if not self.name_entry.validate():
            return

        user = Player(self.name_entry.get())
        user.image_path = f'quince/ui/assets/avatars/avatar01.png'

        npc1 = NPC('Bob')
        npc2 = NPC('Charlie')
        npc3 = NPC('Dana')
        game_frame_factory = GameFrameFactory(user, npc1, npc2, npc3)

        self.start_game(game_frame_factory)


class TopMenuFactory(object):
    """Factory for the top menu object.
    This factory gets injected into the main app so that
    it can create a top menu at runtime and attach it to itself.
    """
    def generate(self, root, start_game):
        """
        Args:
            root (tk widget)
            start_game (function) - Callback function to start
            the game.
        """
        return TopMenu(root, start_game)
