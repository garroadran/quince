"""
A horizontal display of all the cards that
a  player has piled up over the course of a ronda.
"""

import tkinter as tk
from os import getcwd, path
from PIL import Image, ImageTk


IMAGE_ROOT = path.join(getcwd(), "quince/assets/scores/")


class CardScroll(tk.Frame):
    """Horizontal lineup of cards"""
    def __init__(self, parent, player_image, cards, score):
        tk.Frame.__init__(self, parent)

        player_image.thumbnail((65, 65), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(player_image)

        img_label = tk.Label(self, image=img, relief="solid")
        img_label.image = img
        img_label.grid(row=0, column=0, padx=10, sticky="we", rowspan=2)

        self.score_frame = tk.Frame(self)
        self.score_frame.grid(row=1, column=1, sticky="nsew")
        self._draw_score(score)

        self.cards = cards
        self.card_frame = tk.Frame(self)
        self.card_frame.grid(row=1, column=1, sticky="nsew")
        self._draw_cards()
        self.card_frame.tkraise()

        self.visible = self.card_frame

    @property
    def state(self):
        """Descriptor for what is currently visible in the frame."""
        return "Cards" if self.visible is self.card_frame else "Scores"

    def switch_view(self):
        """Raises whichever frame is at the bottom."""
        if self.visible is self.card_frame:
            self.score_frame.tkraise()
            self.visible = self.score_frame
        elif self.visible is self.score_frame:
            self.card_frame.tkraise()
            self.visible = self.card_frame

    def _draw_cards(self):
        """Renders images and places them on the canvas."""
        row = 0
        col = 0

        count = len(self.cards)
        # this should restrict things to two lines in most cases
        line_break_col = 8 if count < 17 else 12

        for card in self.cards:
            resized = card.image()
            resized.thumbnail((65, 65), Image.ANTIALIAS)

            image = ImageTk.PhotoImage(resized)
            lbl = tk.Label(self.card_frame, image=image)
            lbl.image = image
            lbl.grid(row=row, column=col, sticky="we")

            # split over two lines if holding more than 14 cards
            if count > 14 and col >= line_break_col:
                col = 0
                row += 1
            else:
                col += 1

    def _draw_score(self, score):
        """Renders an image with the player's score on it."""
        num = min(score, 30)
        png = Image.open(path.join(IMAGE_ROOT, f"{num}.png"))
        img = ImageTk.PhotoImage(png)
        lbl = tk.Label(self.score_frame, image=img)
        lbl.image = img
        lbl.pack(side="left", anchor="w")
