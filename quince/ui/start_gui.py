#!/usr/bin/env python

"""Graphical application initialization
"""
from quince.ui.game_app import GameApp
from quince.ui.about import AboutFactory
from quince.ui.top_menu.top_menu import TopMenuFactory
from quince.ui.score_report.score_report import ScoreReport


def start():
    """Launch the GUI"""
    about = AboutFactory()
    top_menu = TopMenuFactory()

    app = GameApp(about, top_menu, ScoreReport)

    app.mainloop()
