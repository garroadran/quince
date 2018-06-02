"""
The Card object represents a Card. Each card has a number, and a suit or "palo".
"""

class Card(object):
    """
    The Card object represents a Card. Each card has a number, and a suit or "palo".
    """

    def __init__(self, number, suit):
        """Instatiates a Card object.

        Args:
            number (int) -- Number on the card
            suit (str) -- Card suit
        """
        if number < 1 or number > 10:
            raise ValueError('Cards can only be between 1 and 10')

        self._number = number
        self._suit = suit
        self._image = 'default.png'

        setenta = [0, 0, 0, 0, 0, 0, 10, 0, 0, 0]
        self.points_setenta = setenta[number - 1]

    def __str__(self):
        return str((self._number, self._suit))

    def __repr__(self):
        return str((self._number, self._suit))

    def image(self):
        """Getter for the card's image
        """
        return self._image

    def info(self):
        """Getter for the number and suit of the card.

        Returns:
            Tuple containing (number, suit)
        """
        return (self._number, self._suit)


    def clone(self):
        """Clones a Card object"""
        return Card(self._number, self._suit)
