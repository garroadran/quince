"""
The Card object represents a Card.
Each card has a number, and a suit or "palo".
"""
import os as os
from PIL import Image


SETENTA_SCORING = [11.0, 4.0, 6.0, 8.0, 10.0, 14.0, 17.5, 1, 1, 1]


class Card(object):
    """
    The Card object represents a Card.
    Each card has a number, and a suit or "palo".
    """
    def __init__(self, value, suit):
        """Instatiates a Card object.

        Args:
            number (int) -- Number on the card
            suit (str) -- Card suit
        """
        if value < 1 or value > 10:
            raise ValueError("Cards can only be between 1 and 10")

        self.number = value
        self.suit = suit

        # Values 8, 9, and 10 use the card images numbered 10, 11, 12
        img_num = value if value < 8 else value + 2
        self._image = f"quince/assets/cards/card_{suit}_{img_num}.png"

        self.points_setenta = SETENTA_SCORING[value - 1]

    def image(self):
        """Getter for the card's image"""
        path = os.path.join(os.getcwd(), self._image)
        return Image.open(path)

    def clone(self):
        """Clones a Card object"""
        return Card(self.number, self.suit)

    def __hash__(self):
        hashable = f"{self.number}{self.suit}"
        return hash(hashable)

    def __str__(self):
        return str((self.number, self.suit))

    def __repr__(self):
        return str((self.number, self.suit))

    def __eq__(self, other):
        return self.number == other.number and self.suit == other.suit
