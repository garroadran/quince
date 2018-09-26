"""
Display logic for the cards that are laid face-up on the table.
"""
import tkinter as tk
import math as math
from PIL import Image, ImageTk, ImageEnhance


class Table(tk.Frame):
    """
    A container for a set of cards laid face-up on the table.
    """
    def __init__(self, parent, cards):
        """
        Args:
            parent (tk widget) - Element on which to render the frame
            cards (List of Card)
        """
        tk.Frame.__init__(self, parent)

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
                             indicatoron=False,
                            )

        btn.image = unselected_img
        btn.selected_image = selected_img
        return btn


class GridPosition(object):
    """Specifies a zero-indexed, two-dimensional coordinate point.
    """
    def __init__(self, column_count):
        """Instantiates a GridPosition object with column_count columns.

        Args:
            column_count (int) - Positive integer
        """
        if column_count < 0:
            raise AttributeError("Cannot have a negative amount of columns")

        self.column_count = column_count
        self.row = 0
        self.column = 0

    def get_value(self):
        """Getter for the current position. Returns a tuple of (row, column)
        """
        return self.row, self.column

    def increment_right(self):
        """Moves one position over to the right. If the last column is reached,
        wraps around to the next row.

        Returns:
            A tuple indicating the current position, after the increment (row, column)
        """
        if self.column == self.column_count - 1:
            self.column = 0
            self.row += 1
        else:
            self.column += 1

        return self.get_value()
