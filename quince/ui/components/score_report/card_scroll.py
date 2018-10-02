"""
A horizontal display of all the cards that
a  player has piled up over the course of a ronda.
"""

import tkinter as tk
from PIL import Image, ImageTk


class CardScroll(tk.Frame):
    """Horizontal lineup of cards"""
    def __init__(self, parent, player_image, cards):
        tk.Frame.__init__(self, parent)

        player_image.thumbnail((65, 65), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(player_image)

        img_label = tk.Label(self, image=img, relief='solid')
        img_label.image = img
        img_label.grid(row=0, column=0, padx=10, sticky="we", rowspan=2)

        self.cards = cards
        self._draw_cards(1)

    def _draw_cards(self, starting_col):
        """Renders images and places them on the canvas."""
        row = 0
        col = starting_col

        midpoint = len(self.cards)//2

        for card in self.cards:
            resized = card.image()
            resized.thumbnail((65, 65), Image.ANTIALIAS)

            image = ImageTk.PhotoImage(resized)
            lbl = tk.Label(self, image=image)
            lbl.image = image
            lbl.grid(row=row, column=col, sticky="we")

            # split over two lines if holding more than 14 cards
            if midpoint > 7 and col >= 7:
                col = starting_col
                row += 1
            else:
                col += 1
