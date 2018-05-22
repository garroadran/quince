"""
A ronda is the shortest possible complete segment of a game,
from initial deal to points calculation.

A ronda is played in the following manner:

Players play in clockwise order, starting from the left of the dealer
(the dealer always plays last). During their turn each player can either:

a) Use one of the cards they have in their hand to pick up cards from the mesa
b) Lay down one of their cards on the mesa

The ronda starts by dealing 4 cards to the mesa, and 3 cards to each player.

Note: If the 4 cards that got dealt to the mesa add up to 15, they
are awarded to the dealer immediately along with an escoba, and not replaced.
The ronda begins with an empty table

Then, each player takes their turn, repeating 3 times around until the
players have used all of the cards in their hand.

At this point, the dealer once again deals 3 cards to each player, and
play continues in the same manner.

The ronda ends when all the cards in the deck have been dealt out.

Once all players have played all their cards, any cards that remain
on the mesa will be awarded to the player who last picked up cards.

A complete game will have as many rondas as necessary
until one player reaches a total of 30 points.
"""

from quince.ronda import RondaFinishedError, RondaNotFinishedError

class Ronda(object):
    """Represents one play through a single deck of cards."""

    def __init__(self, players, dealer, deck):
        """Instantiate a ronda object.

        Args:
            players (list of Player) -- The players in the game
            dealer (Player) -- The player who will deal the cards
            deck (Deck) -- The deck to use

        Attributes:
            _players is the list of players in the game
            _DEALER is the index of the player who dealt the cards in the players array
            _deck, a Deck object from which cards are popped out (ie. dealt out)
            _finished keeps track of whether all the cards have been played
            _last_picked_up reference to the last player to pick up cards. That
            person gets the remaining cards on the mesa when the ronda is finished.
            _dealt_escoba remembers whether an escoba was dealt on the first deal of
            4 cards to the mesa.
            _mesa is the cards on the table at the present time
        """
        self._players = players
        self._dealer = players.index(dealer)
        self._deck = deck
        self._last_picked_up = dealer
        self._dealt_escoba = False
        self._mesa = deck.deal(4)

        # check whether a straight escoba has been dealt
        mesa_sum = sum([x.info()[0] for x in self._mesa])
        if mesa_sum == 15:
            # make sure to pass a copy to the dealer's pila, otherwise
            # the cards could be removed from his hand when we clear them here
            self._players[self._dealer].pila().add(self.current_mesa, True)
            self._mesa = []
            self._dealt_escoba = True

        # deal three cards to each player
        self._deal_hands()

        # establish who plays first
        self._current_player = self._dealer
        self._next_player()

    @property
    def current_mesa(self):
        """Returns a copy of the cards on the mesa"""
        return self._mesa[:]

    @property
    def current_player(self):
        """Reference to the player whose turn it is to play.
        """
        return self._players[self._current_player]

    @property
    def dealt_escoba(self):
        """Getter for the state of the initial deal to the mesa.

        Returns true if the first 4 cards that were dealt to the mesa
        added up to 15 (in which case, they should be added automatically
        to the dealer's pila, along with an escoba).
        """
        return self._dealt_escoba

    @property
    def is_finished(self):
        """Returns True if the deck is empty and all players have played their last cards.
        """
        return self._hand_is_done and not self._deck.cards()

    def play_turn(self, own_card, mesa_cards=None):
        """Cause the current player to perform an action, and then pass
        the turn to the next player.

        If a player picks up cards, the _last_picked_up attribute is modified to point
        to the current player.

        Args:
            own_card (Card info tuple) -- What card from their own hand the user will use.
            mesa_cards (List of card info tuples) -- The cards to pick up
        """
        if self.is_finished:
            raise RondaFinishedError()

        # First, the current player performs an action
        if mesa_cards == [] or mesa_cards is None:
            self.current_player.place_card_on_mesa(self._mesa, own_card)
        else:
            self.current_player.pick_up_from_mesa(self._mesa, own_card, mesa_cards)
            self._last_picked_up = self.current_player

        # Then we branch:
        # If the entire ronda is done
        if self.is_finished:
            # the last player to pick up cards gets what remains on the mesa
            self._last_picked_up.pila().add(self.current_mesa)

        # If the hand is done but there are still cards to be dealt
        elif self._hand_is_done:
            self._deal_hands()
            self._next_player()

        # If the hand is not yet done
        else:
            self._next_player()

    def _deal_hands(self):
        """Deals a hand to each player in the game

        Modifies the _deck attribute and the cards in each player's .current_hand
        """
        if self.is_finished:
            raise RondaFinishedError()

        for plyr in self._players:
            plyr.pick_up_hand(self._deck.deal(3))

    @property
    def _hand_is_done(self):
        """Returns True if all players currently have empty hands. False otherwise."""
        for player in self._players:
            if player.current_hand():
                return False        
        return True

    def _next_player(self):
        """Iterates over the players list, and updates the
        _current_player attribute.
        """
        self._current_player = (self._current_player + 1) % len(self._players)
