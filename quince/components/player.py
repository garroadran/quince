"""
Module containing the Player class
"""
import random
import os as os
from PIL import Image
from quince.cpu import enumerate_possibilities
from quince.components.pila import Pila


class Player(object):
    """Represents a player in the game.

    A player has a name, a total score they will accumulate
    over the entire game, a hand of cards which they hold, and
    a pila of cards where they accumulate the cards they
    collect over the course of a ronda.
    """

    internal_id = 0
    names_list = ['Alicia', 'Felipe', 'Mariana', 'Pepe', 'Juanita', 'Timoteo']

    def __init__(self, name=None):
        """Instantiates a player for the game.

        The player is assigned an empty hand to start,
        and a pila, where they will accumulate the cards
        that they pick up over the course of a ronda.

        The player is also given a total score of 0 to start.

        Args:
            name (str) -- Player's name
        """
        self._id = Player.internal_id
        Player.internal_id += 1

        if name is None:
            self._name = random.choice(Player.names_list)
        else:
            self._name = name

        # Cards held in hand
        # changes with each ronda
        self._current_hand = []

        # Cards picked up through play
        # Accumulates with each turn, resets when a new deck gets dealt
        self._pila = Pila()

        self._total_score = 0

    def __repr__(self):
        return f'Player, {self.name()}.'

    def __str__(self):
        return f'Player, {self.name()}.'

    @property
    def id(self):
        """Getter for the unique ID assigned to the player.
        Unique IDs ensure that players can be looked up even
        if their display names match.
        """
        return self._id

    def image(self):
        """Getter for the player's avatar image
        Returns:
            PIL Image object
        """
        path = os.path.join(os.getcwd(), f'ui/assets/avatars/{self.name().lower()}.png')

        if not os.path.exists(path):
            # to do: replace with a proper stock image
            path = 'ui/assets/avatars/alice.png'

        return Image.open(path)

    def name(self):
        """Getter for the player's name
        """
        return self._name

    def total_score(self):
        """Getter for the player's total score
        """
        return self._total_score

    def award_points(self, points=1):
        """Adds points to the player's total score.

        Args:
            points (int) -- Number of points to award (default=1)
        """
        self._total_score += points

    def __hash__(self):
        """Hash function for the player object"""
        return hash(self._name) * self.id

    def __eq__(self, other):
        """Evaluates two players as equal if they share the same id"""
        return self.id == other.id


class NPC(Player):
    """A computer player"""

    @staticmethod
    def get_move(hand, mesa):
        """Select a move for the NPC to make.

        Args:
            hand -- List of card objects
            mesa -- List of card objects

        Returns:
            Tuple containing a card info tuple in the 0th position
            (representing the card to be played from the player's hand),
            and a list of card info tuples in the 1st position
            (representing the cards to be picked up from the mesa).
        """
        possibilities = enumerate_possibilities(mesa, hand)

        # If there's no way to add to 15, select a random card
        # from the hand and drop it
        if not possibilities:
            return (random.choice(hand), [])

        move = random.choice(possibilities)

        from_hand = None
        from_mesa = []

        for card in move:
            if card in hand:
                from_hand = card
            else:
                from_mesa.append(card)

        return (from_hand, from_mesa)
