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
from os import getcwd
from os.path import join
from PIL import Image, ImageTk
from quince.components import Player, NPC
from quince.ui.top_menu.avatar_picker import AvatarPicker
from quince.ui.game_frame_factory import GameFrameFactory
from quince.ui.top_menu.validating_entry import UserNameEntry


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

        self.grid_rowconfigure(0, weight=1)  # header pad
        self.grid_rowconfigure(1, weight=0)  # avatar + username label
        self.grid_rowconfigure(2, weight=0)  # avatar + username entry
        self.grid_rowconfigure(3, weight=0)  # avatar label
        self.grid_rowconfigure(4, weight=0)  # start game btn
        self.grid_rowconfigure(5, weight=1)  # footer pad
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        self.avatar_path = None
        self.avatar = tk.Label(self, text="")
        self.set_avatar(join(getcwd(),
                        "quince/assets/avatars/avatar01.png"))
        avatar_label = tk.Label(self,
                                text="Click to edit",
                                font=("Helvetica", 8))
        avatar_label.grid(row=3, column=1)

        name_entry_label = tk.Label(self, text="Player Name:")
        name_entry_label.grid(row=1, column=2)
        self.name_entry = UserNameEntry(self,
                                        value="Alice",
                                        justify="center",
                                        char_limit=12)
        self.name_entry.grid(row=2, column=2)

        btn = tk.Button(self, text="New Game", command=self._start_game)
        btn.grid(row=4, column=1, columnspan=2, pady=64)

    def _display_avatar(self):
        image = Image.open(self.avatar_path)
        image.thumbnail((65, 65), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        self.avatar.destroy()
        self.avatar = tk.Label(self,
                               image=img,
                               cursor="hand2",
                               highlightbackground="black",
                               highlightthickness=1)
        self.avatar.image = img
        self.avatar.grid(row=1, column=1, padx=32, rowspan=2)
        self.avatar.bind("<Enter>", self.on_avatar_enter)
        self.avatar.bind("<Leave>", self.on_avatar_leave)
        self.avatar.bind("<Button-1>", self.launch_avatar_picker)

    # pylint: disable=unused-argument
    def on_avatar_enter(self, event):
        """Hoverover event for the currently selected avatar image"""
        self.avatar.config(highlightbackground="firebrick3")

    # pylint: disable=unused-argument
    def on_avatar_leave(self, event):
        """Hoverover event for the currently selected avatar image"""
        self.avatar.config(highlightbackground="black")

    def _start_game(self):
        """Wraps the callback function provided by the parent GameApp widget.
        Provides the parent with a list of players which it can use to
        initiate a new game.
        """
        if not self.name_entry.validate():
            return

        user = Player(self.name_entry.get())
        user.set_image(self.avatar_path)

        path = join(getcwd(), "quince/assets/avatars")
        npc1 = NPC("Roberto", f"{path}/avatar06.png")
        npc2 = NPC("Gus", f"{path}/avatar08.png")
        npc3 = NPC("Diana", f"{path}/avatar07.png")
        game_frame_factory = GameFrameFactory(user, npc1, npc2, npc3)

        self.start_game(game_frame_factory)

    def set_avatar(self, path):
        """Sets a different avatar that the user can use in-game

        Args:
            path (string) - Absolute path to the avatar image
        """
        self.avatar_path = path
        self._display_avatar()

    def launch_avatar_picker(self, _):
        """Launches a popup window where the user can select an image
        """
        AvatarPicker(self, self.set_avatar)


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
