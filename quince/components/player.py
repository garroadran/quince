"""
Module containing the Player class
"""
from quince.components.pila import Pila

class Player(object):
    """Represents a player in the game.

    A player has a name, a total score they will accumulate over the entire game,
    a hand of cards which they hold, and a pila of cards where they accumulate
    the cards they collect over the course of a ronda.
    """
    def __init__(self, name):
        """Instantiates a player for the game.

        The player is assigned an empty hand to start,
        and a pila, where they will accumulate the cards
        that they pick up over the course of a ronda.

        The player is also given a total score of 0 to start.

        Args:
            name (str) -- Player's name
        """
        # persistent attribute
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

    def name(self):
        """Getter for the player's name
        """
        return self._name

    def pila(self):
        """Getter for the player's current pila
        """
        return self._pila

    def current_hand(self):
        """Returns a copy of the hand the player is currently holding.
        """
        return self._current_hand[:]

    def total_score(self):
        """Getter for the player's total score
        """
        return self._total_score

    def pick_up_hand(self, hand):
        """Collect a hand from the deck.

        Args:
            hand -- A List of 3 Cards
        """

        self._current_hand = hand

    def holds_card(self, card):
        """Test to see whether the player holds a card in their current hand.

        Args:
            card (tuple) -- Card info in (number, palo) format

        Returns:
            True if the player is currently holding the card, false otherwise
        """
        for card_in_hand in self.current_hand():
            if card == card_in_hand.info():
                return True

        return False

    def place_card_on_mesa(self, mesa, card):
        """Remove a card from the player's hand and place it on the table.

        Modifies the player's "currentHand" attribute and the mesa that was passed.
        Raises a ValueError if the player does not currently own the card.

        During the player's turn, they may put a card
        on the table instead of picking up a combination.
        This is mandatory if the player has no combinations
        that they can pick up, but can also be done in other
        rare circumstances.

        Args:
            mesa (list) -- List of cards on the table
            card (tuple) -- The card to put down (number, palo)
        """
        for i in range(0, len(self._current_hand)):
            if card == self._current_hand[i].info():
                popped_card = self._current_hand.pop(i)
                mesa.append(popped_card)
                return

        raise ValueError('Player is not currently holding ' + str(card))

    def pick_up_from_mesa(self, mesa, own_card, mesa_cards):
        """Remove a single card from the player's current hand,
        and other cards from the mesa in order to add up to 15.
        Place all of these cards in the player's pila.

        Args:
            own_card (number, palo) -- A card that the player currently holds
            mesa_cards -- List of cards in (number, palo) format to remove from the mesa
        """
        # Verify that the sum is OK to pick up
        mesa_amount = 0
        for card in mesa_cards:
            mesa_amount += card[0]
        if mesa_amount + own_card[0] != 15:
            raise ValueError('Tried to pick up cards that don\'t add to 15.')

        # Verify that the cards exist in the correct locations
        if not self.holds_card(own_card):
            raise ValueError('Player does not have a ' + str(own_card) + ' to drop.')

        mesa_cards_info = [x.info() for x in mesa]
        for card_info in mesa_cards:
            if card_info not in mesa_cards_info:
                raise ValueError('Tried to pick up cards that are not available on the mesa.')


        # Pick up the cards
        picked_up_cards = []
        for i in range(len(mesa) - 1, -1, -1):
            if mesa[i].info() in mesa_cards:
                picked_up_cards.append(mesa.pop(i))

        # Add in the player's own card
        for i in range(0, len(self._current_hand)):
            if self._current_hand[i].info() == own_card:
                picked_up_cards.append(self._current_hand.pop(i))
                break # Need to break because it's iterating in ascending order

        is_escoba = len(mesa) == 0

        self._pila.add(picked_up_cards, is_escoba)
