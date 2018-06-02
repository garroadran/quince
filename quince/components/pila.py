"""
Module containing the Pila object
"""

import copy as copy

class Pila(object):
    """A pila ("pile") represents the cards that a player accumulates
    as they play through a round. When a player has their turn, they
    can play one of the cards in their hand to combine with other
    cards, adding up to 15. If they manage to do this, those cards
    that were used in the combination are added to their pila.

    If, in picking up their combination, the player also manages
    to remove the last card from the table, this is called an "escoba,"
    and counts as an additional point.
    """
    def __init__(self):
        """Creates a data structure for tallying up the cards that a player has collected.

        Cards are organized by suit in order to make it easier to tally up scores
        Any changes made here will probably also need to be made to the reset() function
        """
        self._cards = {'oro': [], 'basto': [], 'espada': [], 'copa': []}

        # number of escobas scored
        self._escobas = 0


    def add(self, cards, escoba=False):
        """Take a list of cards and add them to the pila.

        Args:
            cards -- List of cards
            escoba (bool) -- True if the pickup was an escoba
        """
        for card in cards:
            palo = card.info()[1]
            self._cards[palo].append(card)

        if escoba:
            self._escobas += 1


    def get_cards(self):
        """Returns a copy of the cards currently in the pila

        Returns:
            Dictionary of cards sorted by suit
        """
        return copy.deepcopy(self._cards)


    def get_escobas(self):
        """Returns the number of Escobas the player has made
        """
        return self._escobas


    def setenta(self):
        """Calculates the total setenta score in the pila.

        Returns
            A tuple containing an integer representing the score for the setenta,
            and a list containing the cards that were used to make it up.
        """
        cards = self.get_cards()

        # Setenta requires at least 1 card from each suit
        has_empty_suit = [] in cards.values()
        if has_empty_suit:
            return (0, [])

        best_cards_in_each_suit = [max(suit, key=lambda x: x.points_setenta) for suit in cards.values()]
        score = sum([card.points_setenta for card in best_cards_in_each_suit])
        return (score, best_cards_in_each_suit)


    def has_siete_de_belo(self):
        """Returns True if the pila contains the 7 of oro
        """
        for card in self._cards['oro']:
            if card.info()[0] == 7:
                return True

        return False


    def total_cards(self):
        """Returns the total number of cards the user has picked up.
        """
        amount = 0
        for palo in self._cards:
            amount = amount + len(self._cards[palo])

        return amount


    def total_oros(self):
        """Returns the total number of oros that the user has picked up.
        """
        return len(self._cards['oro'])


    def reset(self):
        """Resets the pila to an empty state.
        """
        self._cards = {'oro': [], 'basto': [], 'espada': [], 'copa': []}
        self._escobas = 0
