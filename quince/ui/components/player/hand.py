"""
Tkinter widget to display the hand that the user
is currently holding and manage its interactions.
"""
import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance

CARD_SIZE = (104, 160)
CARD_PADX = 2

class PlayerHand(tk.Frame):
    """
    Represents a frame on the UI where the user can see
    what cards they currently own, and select one to play.
    """
    def __init__(self, parent, cards):
        """
        Args:
            parent (tk.Frame) - Tk Widget
            cards (list) - A list of cards held in the player's hand.

        Properties:
            selected - A card that the user has selected. Can be None.
        """
        tk.Frame.__init__(self, parent)

        if len(cards) > 3:
            raise AttributeError("Too many cards in hand.")

        self.grid_rowconfigure(0, weight=1)

        self.cards = cards
        self._selected_index = tk.IntVar()

        col_width = 2 + CARD_SIZE[0] + CARD_PADX * 2

        for column in range(0, 3):
            self.grid_columnconfigure(column, weight=1, minsize=col_width)

            try:
                card = self.cards[column]
                self._display_card(card, column)
            except IndexError:
                pass


    def _display_card(self, card, column):

        resized = card.image().resize(CARD_SIZE, Image.ANTIALIAS)

        decolor = ImageEnhance.Color(resized)
        decolorized = decolor.enhance(0.2)

        unselected_img = ImageTk.PhotoImage(decolorized)
        selected_img = ImageTk.PhotoImage(resized)

        btn = tk.Radiobutton(
            self,
            image=unselected_img,
            selectimage=selected_img,
            variable=self._selected_index,
            value=column,
            indicatoron=0,
            highlightthickness=0,
            borderwidth=0,
            relief="flat",
            selectcolor="",
            )
        btn.unselected_image = unselected_img
        btn.selected_image = selected_img

        btn.grid(row=0, column=column, padx=CARD_PADX)

    def selected_card(self):
        """Getter for the card that the user has selected."""
        return self.cards[self._selected_index.get()]
