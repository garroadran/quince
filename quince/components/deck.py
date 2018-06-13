"""
Module containing the Deck class, for creating a deck of cards.
"""
import random as random

class Deck(object):
    """
    A Deck represents a deck of cards. When the constructor is called,
    it generates a deck in randomized order.

    Subsequent calls to .deal will deal out cards from the end of the deck.
    """

    def __init__(self, Card, clone=None):
        """Builds a deck of 40 cards using the passed type.

        Cards are provided numbers from 1 to 11, and standard suits.
        Once the deck is built, it is shuffled so that later operations
        can easily pop cards off the end in constant time.

        Args:
            Card -- A class of card to deal
            clone (Deck object) - An existing deck to clone.
        """
        self._card_type = Card;

        if clone is None:
            self._build_new_deck()
            return
        else:
            self._cards = clone.cards()

        
    def _build_new_deck(self):
        self._cards = []

        for i in range(0, 10):
            # Sotas, caballos, and reyes are represented
            # using their real value, not their face number
            for suit in ['oro', 'basto', 'espada', 'copa']:
                new_card = self._card_type(i + 1, suit)
                self._cards.append(new_card)

        # shuffle the deck so that cards can be popped off the end
        random.shuffle(self._cards)


    def __str__(self):
        return f'Deck containing {len(self.cards())} Cards.'


    def __repr__(self):
        return f'Deck containing {len(self.cards())} Cards.'


    def cards(self):
        """Returns a copy of the list of cards in the deck.
        """
        return [x.clone() for x in self._cards]


    def deal(self, amount):
        """Removes cards from the deck and returns a tuple containing a new deck
        and the hand that was dealt.

        Args:
            amount (int) -- Amount of cards to deal

        Returns:
            Tuple (Deck, List of Card).
        """
        hand = [x.clone() for x in self._cards[:amount]]
        self._cards = self._cards[amount:]
        newdeck = Deck(self._card_type, clone=self)
        
        return (newdeck, hand)
