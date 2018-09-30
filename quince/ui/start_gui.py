#!/usr/bin/env python

"""
    Graphical application initialization
"""
from quince.ui.components.game_app import GameApp
from quince.ui.components.about import AboutFactory
from quince.ui.components.top_menu.top_menu import TopMenuFactory

def start():
    """Launch the GUI"""
    about = AboutFactory()
    top_menu = TopMenuFactory()

    app = GameApp(about, top_menu)

    app.mainloop()
