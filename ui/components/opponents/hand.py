"""
Visual display for the cards in the opponent's hand.
Always shows the backs of the cards only.
"""
import tkinter as tk
import os
from PIL import Image, ImageTk


class OpponentHand(tk.Frame):
    """
    A frame containing for an image that shows an opponent's hand (i.e., the backs)
    of the cards.
    """
    def __init__(self, parent, number_of_cards, size=150):
        """
        Creates a frame that shows how many cards the opponent is holding.

        Args:
            parent (tk.Frame) - Parent frame/container to which this frame attaches
            number_of_cards (int) - An int between 0 and 3
        """
        if number_of_cards < 0 or number_of_cards > 3:
            raise AttributeError("Invalid number of cards in opponent's hand. \
                                 Should be between 0 and 3")

        tk.Frame.__init__(self, parent, background="green")

        relpath = f'ui/assets/opponent_hands/cards_{number_of_cards}.png'
        image_path = os.path.join(os.getcwd(), relpath)
        orig = Image.open(image_path)
        img = orig.resize((size, size), Image.ANTIALIAS)
        card_backs = ImageTk.PhotoImage(img)

        label = tk.Label(self, image=card_backs)
        label.image = card_backs # hold on to the reference
        label.pack()
