"""
    Graphical application initialization
"""
from ui.components.game_app import GameApp
from ui.components.game_frame_factory import GameFrameFactory
from quince.components import Player, NPC

TINA = Player('Tina')
BOB = NPC('Bob')
CHARLIE = NPC('Charlie')
DANA = NPC('Dana')
FACTORY = GameFrameFactory(TINA, BOB, CHARLIE, DANA)

APP = GameApp(FACTORY)

APP.frames['GameFrame'].draw()
APP.frames['GameFrame'].play_next_move()

APP.mainloop()
