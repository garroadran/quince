#!/usr/bin/env python

"""
    Graphical application initialization
"""
from ui.components.game_app import GameApp
from ui.components.about import AboutFactory
from ui.components.top_menu import TopMenuFactory

ABOUT_FACTORY = AboutFactory()
TOP_MENU_FACTORY = TopMenuFactory()

APP = GameApp(ABOUT_FACTORY, TOP_MENU_FACTORY)

APP.mainloop()
