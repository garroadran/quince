"""
The Card object represents a Card.
Each card has a number, and a suit or "palo".
"""
import os as os
from PIL import Image


class Card(object):
    """
    The Card object represents a Card.
    Each card has a number, and a suit or "palo".
    """

    def __init__(self, number, suit):
        """Instatiates a Card object.

        Args:
            number (int) -- Number on the card
            suit (str) -- Card suit
        """
        if number < 1 or number > 10:
            raise ValueError("Cards can only be between 1 and 10")

        self._number = number
        self.number = number
        self._suit = suit
        self.suit = suit

        img_num = number
        if img_num >= 8:
            img_num += 2

        self._image = f"quince/assets/cards/card_{suit}_{img_num}.png"

        setenta = [11.0, 4.0, 6.0, 8.0, 10.0, 14.0, 17.5, 1, 1, 1]
        self.points_setenta = setenta[number - 1]

    def __str__(self):
        return str((self.number, self.suit))

    def __repr__(self):
        return str((self.number, self.suit))

    def __eq__(self, other):
        return self.number == other.number and self.suit == other.suit

    def image(self):
        """Getter for the card's image
        """
        path = os.path.join(os.getcwd(), self._image)
        return Image.open(path)

    def info(self):
        """Getter for the number and suit of the card.

        Returns:
            Tuple containing (number, suit)
        """
        return (self.number, self.suit)

    def clone(self):
        """Clones a Card object"""
        return Card(self.number, self.suit)

    def __hash__(self):
        hashable = f"{self.number}{self.suit}"
        return hash(hashable)
