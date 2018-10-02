"""
    Factory object that gets used to inject dependencies
    into the GameApp constructor.
"""
from quince.ui.components.game_frame import GameFrame


class GameFrameFactory(object):
    """Creates a GameFrame object.
    By passing this factory to the GameApp constructor,
    we can inject dependencies via the factory as necessary,
    and only instantiate the GameFrame when its parent widget
    (ie. the GameApp itself) is already instantiated.
    """
    def __init__(self, player, npc1, npc2, npc3):
        self.player = player
        self.npc1 = npc1
        self.npc2 = npc2
        self.npc3 = npc3

    def generate(self, root, callback):
        """Generates a GameFrame object whose parent Tk widget is 'root'.

        Args:
            root (Tk widget)
        """
        return GameFrame(root, self.player, self.npc1, self.npc2, self.npc3, callback)
