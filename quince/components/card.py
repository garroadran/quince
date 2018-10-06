"""
The Card object represents a Card.
Each card has a value and a suit.
"""
from os import path, getcwd
from PIL import Image


SETENTA_SCORING = [11.0, 4.0, 6.0, 8.0, 10.0, 14.0, 17.5, 1, 1, 1]


class Card(object):
    """
    The Card object represents a Card.
    Each card has a value and a suit.
    """
    def __init__(self, value, suit):
        """Instatiates a Card object.

        Args:
            value (int) -- Number on the card
            suit (str) -- Card suit
        """
        if value < 1 or value > 10:
            raise ValueError("Cards can only be between 1 and 10")

        self.value = value
        self.suit = suit

        # Values 8, 9, and 10 use the card images numbered 10, 11, 12
        img_num = value if value < 8 else value + 2
        self._image = f"quince/assets/cards/card_{suit}_{img_num}.png"

        self.points_setenta = SETENTA_SCORING[value - 1]

    def image(self):
        """Getter for the card's image"""
        img_path = path.join(getcwd(), self._image)
        return Image.open(img_path)

    def clone(self):
        """Clones a Card object"""
        return Card(self.value, self.suit)

    def __str__(self):
        return str((self.value, self.suit))

    def __repr__(self):
        return str((self.value, self.suit))

    def __hash__(self):
        hashable = f"{self.value}{self.suit}"
        return hash(hashable)

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit
