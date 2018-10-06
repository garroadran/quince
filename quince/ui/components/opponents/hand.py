"""
Visual display for the cards in the opponent's hand.
Always shows the backs of the cards only.
"""
import tkinter as tk
from os import getcwd
from os.path import join
from PIL import Image, ImageTk


class OpponentHand(tk.Frame):
    """A frame containing for an image that shows
    an opponent's hand (i.e., the backs) of the cards.
    """
    def __init__(self, parent, number_of_cards, size=100):
        """Creates a frame that shows how many cards the opponent is holding.

        Args:
            parent (tk.Frame) - Parent frame/container
            number_of_cards (int) - An int between 0 and 3
        """
        if number_of_cards < 0 or number_of_cards > 3:
            raise AttributeError("Invalid number of cards in opponent's hand. \
                                 Should be between 0 and 3")

        tk.Frame.__init__(self, parent)

        self.image_size = size
        self.card_count = number_of_cards
        self.label = tk.Label(self)
        self.label.pack()
        self.refresh(number_of_cards)

    def _get_card_backs_image(self):
        path = f"quince/assets/opponent_hands/cards_{self.card_count}.png"
        image_path = join(getcwd(), path)
        image = Image.open(image_path)
        image.thumbnail((self.image_size, self.image_size), Image.ANTIALIAS)
        return image

    def _overlay_images(self, layer1, layer2):
        final = Image.new("RGBA", layer1.size)
        final = Image.alpha_composite(final, layer1)
        final = Image.alpha_composite(final, layer2)
        return final

    def flash_card(self, card):
        self.card_count -= 1
        card_backs = self._get_card_backs_image()

        card_base = Image.new("RGBA", card_backs.size)

        card_face = card.image().copy()
        resize = (card_base.size[0] * 0.9, card_base.size[1] * 0.9)
        card_face.thumbnail(resize, Image.ANTIALIAS)
        card_base.paste(card_face, (20, 8))

        overlayed = self._overlay_images(card_backs, card_base)
        final = ImageTk.PhotoImage(overlayed)
        self.label.config(image=final)
        self.image = final

    def refresh(self, card_count):
        """Redraws the widget with the correct number of cards.

        Args:
            card_count (int) - Number of cards currently in hand
        """
        self.card_count = card_count
        backs = self._get_card_backs_image()
        backs = self._overlay_images(backs, backs)
        card_backs = ImageTk.PhotoImage(backs)

        self.label.config(image=card_backs)
        self.image = card_backs  # hold on to the reference
