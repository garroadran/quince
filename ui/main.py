"""
    Graphical application initialization
"""
import time as time
from ui.components.game_app import GameApp
from ui.components.game_frame_factory import GameFrameFactory
from quince.components import Player, NPC

TINA = NPC('Tina')
BOB = NPC('Bob')
CHARLIE = NPC('Charlie')
DANA = Player('Dana')
FACTORY = GameFrameFactory(DANA, TINA, BOB, CHARLIE)

APP = GameApp(FACTORY)

APP.frames['GameFrame'].play_next_move()

APP.mainloop()
