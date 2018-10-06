import unittest
from quince.components import Deck, Card


class TestDeck(unittest.TestCase):
    def test_constructor(self):
        """Takes a Card class and builds a deck of 40 Cards"""
        deck = Deck(Card)
        self.assertEqual(40, len(deck.cards()))

        # Assert that there are no duplicate cards in the deck
        deck_check = {"oro": [], "espada": [], "copa": [], "basto": []}
        for card in deck.cards():
            (number, palo) = card.info()
            if number in deck_check[palo]:
                self.fail("Duplicate card in deck")
            else:
                deck_check[palo].append(number)

        # And that each suit has cards 1-10
        for palo in deck_check:
            for i in range(1, 11):
                if i not in deck_check[palo]:
                    self.fail("Missing " + str(i) + " in " + palo)

    def test_cards(self):
        """Returns a copy of the deck"""
        deck = Deck(Card)
        cards = deck.cards()
        cards[0].number = 20
        self.assertNotEqual(20, deck._cards[0].number)

    def test_deal(self):
        """Returns a new deck object and a hand List
        containing the cards that were dealt"""
        deck = Deck(Card)
        (deck2, hand) = deck.deal(4)
        self.assertEqual(36, len(deck2.cards()))
        self.assertEqual(4, len(hand))

        for c in hand:
            self.assertTrue(c not in deck2._cards)

    def test_str(self):
        """String representation"""
        d = Deck(Card)
        s = str(d)
        self.assertTrue("40" in s)

    def test_repr(self):
        """String representation"""
        d = Deck(Card)
        d.deal(4)
        s = repr(d)
        self.assertTrue("36" in s)

    def test_generate_clone(self):
        """Builds a clone of an existing deck, if one is passed."""
        d1 = Deck(Card)
        d1._cards = d1._cards[20:]

        # instantiate a clone
        d2 = Deck(Card, clone=d1)

        # check that the right cards got passed
        cards_in_d1 = [x.info() for x in d1.cards()]
        cards_in_d2 = [x.info() for x in d2.cards()]
        self.assertEqual(cards_in_d1, cards_in_d2)

        # check that it really is a clone
        d1._cards[0].number = 14
        self.assertNotEqual(14, d2._cards[0].number)
