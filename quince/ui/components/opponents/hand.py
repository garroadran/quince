"""
Visual display for the cards in the opponent's hand.
Always shows the backs of the cards only.
"""
import tkinter as tk
import os
from PIL import Image, ImageTk


class OpponentHand(tk.Frame):
    """
    A frame containing for an image that shows
    an opponent's hand (i.e., the backs) of the cards.
    """
    def __init__(self, parent, number_of_cards, size=100):
        """
        Creates a frame that shows how many cards the opponent is holding.

        Args:
            parent (tk.Frame) - Parent frame/container
            number_of_cards (int) - An int between 0 and 3
        """
        if number_of_cards < 0 or number_of_cards > 3:
            raise AttributeError("Invalid number of cards in opponent's hand. \
                                 Should be between 0 and 3")

        tk.Frame.__init__(self, parent)

        self.image_size = size

        self.label = tk.Label(self)
        self.label.pack()
        self.refresh(number_of_cards)

    def refresh(self, card_count):
        """Redraws the widget with the correct number of cards.

        Args:
            card_count (int) - Number of cards currently in hand
        """
        relpath = f'quince/ui/assets/opponent_hands/cards_{card_count}.png'
        image_path = os.path.join(os.getcwd(), relpath)
        image = Image.open(image_path)
        image.thumbnail((self.image_size, self.image_size), Image.ANTIALIAS)
        card_backs = ImageTk.PhotoImage(image)

        self.label.config(image=card_backs)
        self.image = card_backs  # hold on to the reference
