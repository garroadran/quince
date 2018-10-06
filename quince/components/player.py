"""Module containing the Player class
"""
import random
from os import getcwd, path
from PIL import Image
from quince.cpu import enumerate_possibilities
from quince.components import Pila


STOCK_IMAGE_PATH = path.join(getcwd(), "quince/assets/avatars/avatar01.png")


def load_image(img_path):
    """Loads the image at the path provided, or a stock
    image if the path doesn't exist.

    Args:
        path (string)

    Returns:
        PIL.Image object
    """
    # fallback in case a relative path was passed in
    if not path.exists(img_path):
        print("WARNING: Passing relative paths is deprecated"
              "and will cause errors in future releases.")
        img_path = path.join(getcwd(), img_path)

    if not path.exists(img_path):
        img_path = STOCK_IMAGE_PATH

    return Image.open(img_path)


class Player(object):
    """Represents a player in the game.

    A player has a name, a hand of cards which they hold, and
    a pila of cards where they accumulate the cards they
    collect over the course of a ronda.
    """

    internal_id = 0
    names_list = ["Alicia", "Felipe", "Mariana", "Pepe", "Juanita", "Timoteo"]

    def __init__(self, name, image_path=STOCK_IMAGE_PATH):
        """Instantiates a player for the game.

        The player is assigned an empty hand to start,
        and a pila, where they will accumulate the cards
        that they pick up over the course of a ronda.

        Args:
            name (str) -- Player's name
            image_path (string) -- Path to the image for the player's avatar
        """
        self._id = Player.internal_id
        Player.internal_id += 1

        self.name = name

        # Cards held in hand. Changes with each turn played.
        self._current_hand = []

        # Cards picked up through play
        # Accumulates with each turn, resets when a new deck gets dealt
        self._pila = Pila()

        self._image = load_image(image_path)

    def __repr__(self):
        return f"Player, {self.name}."

    def __str__(self):
        return f"Player, {self.name}."

    @property
    def id(self):
        """Getter for the unique ID assigned to the player.
        Unique IDs ensure that players can be looked up even
        if their display names match.
        """
        return self._id

    @property
    def image(self):
        """Getter for the player's avatar image

        Returns:
            PIL Image object
        """
        return self._image.copy()

    def __hash__(self):
        """Hash function for the player object"""
        return hash(self.id)

    def __eq__(self, other):
        """Evaluates two players as equal if they share the same id"""
        return self.id == other.id


class NPC(Player):
    """A computer player"""

    def get_move(self, hand, mesa):
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
