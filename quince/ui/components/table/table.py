"""
Display logic for the cards that are laid face-up on the table.
"""
import tkinter as tk
import math as math
from PIL import Image, ImageTk, ImageEnhance
from quince.utility import GridPosition


class Table(tk.Frame):
    """
    A container for a set of cards laid face-up on the table.
    """
    def __init__(self, parent, cards, callback):
        """
        Args:
            parent (tk widget) - Element on which to render the frame
            cards (List of Card)
            callback (function) - Callback function to execute when
            the selection of cards on the table has changed.
        """
        tk.Frame.__init__(self, parent)

        self.callback = callback
        self.card_statuses = dict()

        column_count = math.ceil(len(cards)/2)
        grid_position = GridPosition(column_count)
        for card in cards:
            self.card_statuses[card] = tk.BooleanVar()

            btn = self._generate_card_button(card)

            row, col = grid_position.get_value()
            btn.grid(row=row, column=col, padx=2)
            grid_position.increment_right()

    def selected_cards(self):
        """Return a list of cards that the user has selected.
        """
        return [c for c in self.card_statuses if self.card_statuses[c].get() == 1]

    def _notify_selection_changed(self):
        """Uses the callback provided in the constructor to
        notify the caller that the user has selected or deselected a card."""
        self.callback(self.selected_cards())

    def _generate_card_button(self, card):
        resized = card.image()
        resized.thumbnail((140, 140), Image.ANTIALIAS)

        decolor = ImageEnhance.Color(resized)
        decolorized = decolor.enhance(0.2)

        unselected_img = ImageTk.PhotoImage(decolorized)
        selected_img = ImageTk.PhotoImage(resized)

        btn = tk.Checkbutton(self,
                             image=unselected_img,
                             selectimage=selected_img,
                             highlightthickness=1,
                             highlightcolor="red",
                             borderwidth=0,
                             relief="flat",
                             offvalue=0,
                             onvalue=1,
                             variable=self.card_statuses[card],
                             command=self._notify_selection_changed,
                             indicatoron=False,
                            )

        btn.image = unselected_img
        btn.selected_image = selected_img
        return btn
