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
from copy import deepcopy
from quince.components import Pila, Deck, Card
from quince.ronda.points_counters import PointsCounter, SetentaCounter


def deal_to_players(players, deck):
    """Perform an initial deal to a list of players.

    Args:
        players -- List of Player
        deck -- Deck object

    Returns:
        Dictionary with players as keys, and 'hand' and 'pila' keys.
    """
    player_cards = {}
    for player in players:
        (deck, hand) = deck.deal(3)
        player_cards[player] = {
            'hand': hand,
            'pila': Pila()
        }

    return (player_cards, deck)


def get_next_player(players, currentplayer):
    """Returns the next player in an ordered list.
    Cycles around to the beginning of the list if reaching the end.

    Args:
        players -- List
        currentplayer -- Element in the list
    """
    i = players.index(currentplayer) + 1
    return players[i % len(players)]


def remove_card_from_hand(player, card, player_cards):
    """Returns a copy of a player_cards dictionary but with a single card
    removed from the player whose reference was provided.

    Args:
        player - Reference to a Player object that exists as a key
                 in the player_cards dictionary
        card - Card object to remove from that player's hand
        player_cards - Dictionary with player keys.

    Returns:
        Copy of the player_cards dictionary with the card of choice removed
        from that player's hand.
    """
    new_dict = deepcopy(player_cards)
    new_dict[player]['hand'] = remove_cards_from_list([card],
                                                      new_dict[player]['hand'])
    return new_dict


def remove_cards_from_list(cards_to_remove, card_list):
    """Remove a card from a list of Cards and return a copy.

    Args:
        card - Card List of Card objects
        L - List of card objects

    Returns:
        List of Card objects
    """
    return [crd for crd in card_list if crd not in cards_to_remove]


def add_cards_to_pila(player, player_cards, cards):
    """Returns a copy of a player_cards dictionary but with a bunch of cards
    added on to a single player's pila.

    Args:
        player - Player object
        player_cards - Dictionary with player keys
        cards - List of Card

    Returns:
        Copy of the player_cards dictionary.
    """
    new_dict = deepcopy(player_cards)
    new_dict[player]['pila'] = new_dict[player]['pila'].add(cards)
    return new_dict


class Ronda(object):
    """Represents one play through a single deck of cards."""

    # pylint: disable=too-many-instance-attributes
    # 8 is acceptable in this case

    def __init__(self, **kwargs):
        """Instantiates a new Ronda. This method will generally not be used
        by outside clients, as they will usually prefer to instantiate a new
        ronda using the Ronda.start() function.

        Keyword args:
            current_player - Reference to a player
            dealer - Reference to a player
            deck - Deck to be used (can be full or partially empty)
            last_pickup - Reference to the last player to pick up cards
            mesa - List of cards currently on the table
            players - Ordered list of Player (used to track whose turn is next)
            player_cards - Dictionary of Cards belonging to each player
        """
        self.current_player = kwargs.get('current_player', None)
        self._dealer = kwargs.get('dealer', None)
        self.deck = kwargs.get('deck', None)
        self._last_picked_up = kwargs.get('last_pickup', None)
        self._mesa = kwargs.get('mesa', None)
        self._players = kwargs.get('players', [])
        self._player_cards = kwargs.get('player_cards', None)

        # If the entire ronda is done
        if self.is_finished:
            self._player_cards = add_cards_to_pila(self._last_picked_up,
                                                   self._player_cards,
                                                   self._mesa)
            self.mesa = []

        # If the hand is done but there are still cards to be dealt
        elif self._hand_is_done:
            (player_cards, deck) = deal_to_players(self._players, self.deck)
            for player in self._player_cards.keys():
                 player_cards[player]['pila'] = self._player_cards[player]['pila']
            self._player_cards = player_cards
            self.deck = deck

    @classmethod
    def start(cls, players, dealer):
        """Performs all the initial setup for starting to play a ronda.

        Args:
            players (list of Player) -- The players in the game
            dealer (Player) -- The player who will deal the cards

        Returns:
            A new Ronda object.
        """
        # Deal to players
        (player_cards, deck) = deal_to_players(players, Deck(Card))

        # Then to the table,
        # and check whether or not a straight escoba was dealt
        (deck, table_deal) = deck.deal(4)

        if sum([card.number for card in table_deal]) == 15:
            # transfer the cards directly to the dealer's pila
            player_cards[dealer]['pila'] = player_cards[dealer]['pila'] \
                                            .add(table_deal)
            mesa = []
        else:
            mesa = table_deal

        attributes = {
            'current_player': get_next_player(players, dealer),
            'dealer': dealer,
            'deck': deck,
            'last_pickup': dealer,
            'mesa': mesa,
            'players': players,
            'player_cards': player_cards
        }

        return cls(**attributes)

    @property
    def current_mesa(self):
        """Public getter for the current cards on the table

        Returns:
            List of Card objects.
        """
        return [card.clone() for card in self._mesa]

    @property
    def player_cards(self):
        """Public getter for cards owned by all players,
        whether in their hand or on their Pila.

        Returns:
            Dictionary containing a "hand" and "pila" for each player key.
        """
        return self._player_cards

    @property
    def dealer(self):
        """Public getter for the player who is dealing during the ronda.

        Returns:
            Reference to a player object.
        """
        return self._dealer

    @property
    def last_picked_up(self):
        """Public getter for the player who was the last to pick up a card.
        Defaults to the dealer at the start of the round.

        Returns:
            Reference to a Player object.
        """
        return self._last_picked_up

    @property
    def is_finished(self):
        """True if deck is empty and all players have played their last cards.
        """
        return self._hand_is_done and not self.deck.cards()

    def play_turn(self, own_card, mesa_cards=None):
        """Cause the current player to perform an action, and then pass
        the turn to the next player.

        If a player picks up cards, the _last_picked_up attribute
        is modified to point to the current player.

        Once the player has completed their action, the ronda checks its own
        state and decides whether it should move to the next player,
        deal another hand, or finish the ronda altogether.

        Args:
            own_card (Card object) -- Card from the current player's hand
            mesa_cards (List of cards) -- The cards to pick up

        Returns:
            New Ronda object with updated attributes
        """
        if self.is_finished:
            raise RondaFinishedError()

        if not mesa_cards:
            new_player_cards = remove_card_from_hand(self.current_player,
                                                     own_card,
                                                     self._player_cards)
            new_mesa = self.current_mesa
            new_mesa.append(own_card)
        else:
            new_player_cards = remove_card_from_hand(self.current_player,
                                                     own_card,
                                                     self._player_cards)
            new_mesa = remove_cards_from_list(mesa_cards,
                                              self.current_mesa)
            new_player_cards = add_cards_to_pila(self.current_player,
                                                 new_player_cards,
                                                 mesa_cards + [own_card])
            self._last_picked_up = self.current_player

        attributes = {
            'current_player': get_next_player(self._players,
                                              self.current_player),
            'dealer': self.dealer,
            'deck': self.deck,
            'last_pickup': self._last_picked_up,
            'mesa': new_mesa,
            'players': self._players,
            'player_cards': new_player_cards
        }

        return Ronda(**attributes)

    @property
    def _hand_is_done(self):
        """Returns True if all players currently have empty hands."""
        for val in self._player_cards.values():
            if val['hand']:
                return False
        return True

    def calculate_scores(self):
        """Compare all players' pilas and tally scores.

        Single points are awarded for:
        - Most cards
        - Most oros
        - Best Setenta score
        - 7 de velo
        - Each escoba

        This method returns the scores, but does not award them.

        Args:
            players - List of Player

        Returns:
            Dictionary containing records for each of the 5 types of scores.
            'most_cards' is a tuple ([players tied for 1st place], card_count)
            'most_oros' is a tuple ([players tied for 1st place], card_count)
            'setenta' is a list of Setenta winner objects
            '7_de_velo' is a reference to the player who obtained the 7
            'escobas' is a list of tuples (player, escobas_count)
        """
        most_cards = PointsCounter()
        most_oros = PointsCounter()
        setenta = SetentaCounter()

        ronda_points = {
            'escobas': []
        }

        for player in self._player_cards:
            pila = self._player_cards[player]['pila']
            most_cards.compare(player, pila.total_cards())

            most_oros.compare(player, pila.total_oros())

            # This method is not yet implemented
            setenta.compare(player, pila.best_setenta())

            if pila.has_siete_de_velo():
                ronda_points['7_de_velo'] = player

            escobas = pila.get_escobas()
            if escobas > 0:
                ronda_points['escobas'].append((player, escobas))

        ronda_points['most_cards'] = (most_cards.winners, most_cards.top_score)
        ronda_points['most_oros'] = (most_oros.winners, most_oros.top_score)
        ronda_points['setenta'] = setenta.winners

        return ronda_points


class RondaFinishedError(Exception):
    """Error raised when trying to perform an action that can only
    be done if the ronda is still ongoing.
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = "The current ronda is finished."
        super(RondaFinishedError, self).__init__(msg)


class RondaNotFinishedError(Exception):
    """Error raised when trying to perform an action that can only
    be done once the ronda is finished.
    """
    def __init__(self, msg=None):
        if msg is None:
            msg = "The current ronda is not yet finished."
        super(RondaNotFinishedError, self).__init__(msg)
