import tkinter as tk
from ui.components.game_frame_factory import GameFrameFactory
from quince.components import Player, NPC

class TopMenu(tk.Frame):
    def __init__(self, root, start_game):
        tk.Frame.__init__(self, root)

        self.start_game = start_game

        btn = tk.Button(self, text="New Game", command=self._start_game)
        btn.pack()
    
    def _start_game(self):
        """Wraps the callback function provided by the parent GameApp widget.
        Provides the parent with a list of players which it can use to
        initiate a new game.
        """
        TINA = Player('Alice')
        BOB = NPC('Bob')
        CHARLIE = NPC('Charlie')
        DANA = NPC('Dana')
        game_frame_factory = GameFrameFactory(TINA, BOB, CHARLIE, DANA)

        self.start_game(game_frame_factory)

class TopMenuFactory(object):
    def generate(self, root, start_game):
        """
        Args:
            root (tk widget)
            start_game (function) - Callback function to start
            the game.
        """
        return TopMenu(root, start_game)
