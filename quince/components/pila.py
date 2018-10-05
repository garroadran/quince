"""
Module containing the Pila object
"""
from copy import deepcopy


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
    def __init__(self, cards=None, escobas=0):
        """Creates a data structure for tallying up
        the cards that a player has collected.

        Cards are organized by suit in order to make it easier
        to tally up scores.

        Args:
            cards -- Dictionary of cards with which to instantiate the pile
        """
        if cards is None:
            self._cards = {"oro": [], "basto": [], "espada": [], "copa": []}
        else:
            self._cards = deepcopy(cards)

        # number of escobas scored
        self._escobas = escobas

    def add(self, cards, escoba=False):
        """Take a list of cards and return a new pila that includes
        all existing cards in the current pila plus the new ones.

        Args:
            cards -- List of cards
            escoba (bool) -- True if the pickup was an escoba
        """
        existing_cards = self.get_cards()

        for card in cards:
            suit = card.info()[1]
            existing_cards[suit].append(card)

        escobas_count = self._escobas

        if escoba:
            escobas_count += 1

        return Pila(cards=existing_cards, escobas=escobas_count)

    def get_cards(self):
        """Returns a copy of the cards currently in the pila

        Returns:
            Dictionary of cards sorted by suit
        """
        return deepcopy(self._cards)

    @property
    def escobas(self):
        """Returns the number of escobas the player has made
        """
        return self._escobas

    def get_escobas(self):
        """Alias for the escobas property
        """
        return self.escobas

    def best_setenta(self):
        """Calculates the total setenta score in the pila.

        Returns
            A list containing copies of the card objects used to make up
            the player's best possible setenta.
        """
        cards = self.get_cards()

        # Setenta requires at least 1 card from each suit
        has_empty_suit = [] in cards.values()
        if has_empty_suit:
            return []

        best_cards = [max(suit, key=lambda x: x.points_setenta)
                      for suit in cards.values()]
        return best_cards

    def has_siete_de_velo(self):
        """Returns True if the pila contains the 7 of oro
        """
        for card in self._cards["oro"]:
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
        return len(self._cards["oro"])
