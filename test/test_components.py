import unittest
from quince.components import Card, Deck, Player, Pila

class TestCard(unittest.TestCase):
    def test_info(self):
        """Returns a tuple containing suit and number"""
        c = Card(4, 'basto')
        self.assertEqual((4, 'basto'), c.info())

        # Check that an error is raised on an invalid number
        with self.assertRaises(ValueError):
            c = Card(13, 'espada')


    def test_clone(self):
        """Clones a card"""
        c = Card(1, 'oro')
        d = c.clone()

        # Modifying this private attribute just for the purposes of testing
        c._number = 3
        self.assertEqual((1, 'oro'), d.info())

    @unittest.skip("Not implemented")
    def test_image(self):
        """Returns an image for the card"""
        c = Card(10, 'oro')

        self.fail('Failed')

class TestDeck(unittest.TestCase):
    def test_constructor(self):
        """Takes a Card class and builds a deck of 40 Cards"""
        deck = Deck(Card)
        self.assertEqual(40, len(deck.cards()))

        # Assert that there are no duplicate cards in the deck
        deck_check = {'oro': [], 'espada': [], 'copa': [], 'basto': []}
        for card in deck.cards():
            (number, palo) = card.info()
            if number in deck_check[palo]:
                self.fail('Duplicate card in deck')
            else:
                deck_check[palo].append(number)

        # And that each suit has cards 1-10
        for palo in deck_check:
            for i in range(1, 11):
                if not i in deck_check[palo]:
                    self.fail('Missing ' + str(i) + ' in ' + palo)


    def test_cards(self):
        """Returns a copy of the deck"""
        deck = Deck(Card)
        cards = deck.cards()
        cards.append('More cards!')
        self.assertEqual(40, len(deck.cards()))

    def test_deal(self):
        """Deals a random set of cards, and removes them from the deck"""
        deck = Deck(Card)
        deck.deal(4)
        self.assertEqual(36, len(deck.cards()))

        deck.deal(3)
        self.assertEqual(33, len(deck.cards()))

class TestPlayer(unittest.TestCase):
    def test_pick_up_hand(self):
        """Collects a hand of three cards from the deck (ie. at the start of each round)"""
        bob = Player('Bob')
        a = Card(3, 'oro')
        b = Card(4, 'oro')
        c = Card(5, 'oro')
        bob.pick_up_hand([a, b, c])
        self.assertEqual([a, b, c], bob.current_hand())

    def test_name(self):
        """Getter for the player's name"""
        alice = Player('Alice')
        self.assertEqual('Alice', alice.name())

    def test_holds_card(self):
        """True if the player has the card in their current hand"""
        alice = Player('Alice')
        a = Card(3, 'oro')
        b = Card(4, 'oro')
        c = Card(5, 'espada')
        alice.pick_up_hand([a, b, c])

        self.assertTrue(alice.holds_card((3, 'oro')))
        self.assertTrue(alice.holds_card((5, 'espada')))
        self.assertFalse(alice.holds_card((10, 'oro')))
        self.assertFalse(alice.holds_card((4, 'copa')))

    def test_total_score(self):
        """Getter for the player's score"""
        alice = Player('Alice')
        self.assertEqual(0, alice.total_score())

    def test_place_card_on_mesa(self):
        """Puts down a card on the mesa"""
        alice = Player('Alice')
        card1 = Card(5, 'oro')
        card2 = Card(10, 'basto')
        card3 = Card(8, 'espada')
        alice.pick_up_hand([card1, card2, card3])

        mesa = []
        alice.place_card_on_mesa(mesa, (5, 'oro'))
        self.assertEqual(card1, mesa[0])
        self.assertEqual([card2, card3], alice.current_hand())

        alice.place_card_on_mesa(mesa, (8, 'espada'))
        self.assertEqual([card1, card3], mesa)
        self.assertEqual([card2], alice.current_hand())

    def test_pick_up_from_mesa(self):
        """Plays one card from their current hand and picks up
        cards from the mesa, adding up to 15, and places them
        in their pila. If last card is taken from the mesa,
        an escoba is counted.

        Modifies the player's currenthand, pila, and the mesa.
        """
        alice = Player('Alice')
        bob = Player('Bob')
        card_alice1 = Card(5, 'oro')
        card_alice2 = Card(7, 'basto')
        card_alice3 = Card(8, 'espada')
        card_bob1 = Card(5, 'espada')
        card_bob2 = Card(7, 'copa')
        card_bob3 = Card(8, 'oro')
        card_mesa1 = Card(4, 'copa')
        card_mesa2 = Card(4, 'basto')
        card_mesa3 = Card(10, 'oro')

        alice.pick_up_hand([card_alice1, card_alice2, card_alice3])
        bob.pick_up_hand([card_bob1, card_bob2, card_bob3])
        mesa = [card_mesa1, card_mesa2, card_mesa3]

        # Alice uses her 7 to pick up two 4s from the table
        alice.pick_up_from_mesa(mesa, (7, 'basto'), [(4, 'basto'), (4,'copa')])
        self.assertEqual([card_mesa3], mesa)
        self.assertEqual([card_alice1, card_alice3], alice.current_hand())

        # Next, bob uses his 5 to pick up the 10 from the table and get an escoba
        bob.pick_up_from_mesa(mesa, (5, 'espada'), [(10, 'oro')])
        self.assertEqual([], mesa)
        self.assertEqual(1, bob.pila().get_escobas())
        self.assertEqual([card_bob2, card_bob3], bob.current_hand())

class TestPila(unittest.TestCase):
    def test_has_setenta(self):
        """Identifies whether or not the player is able to form a setenta"""
        pila1 = Pila()
        pila2 = Pila()
        basto = Card(4, 'basto')
        oro = Card(7, 'oro')
        espada = Card(10, 'espada')
        copa = Card(1, 'copa')

        pila1.add([basto, oro, espada, copa])
        pila2.add([basto, oro, espada])

        self.assertTrue(pila1.has_setenta())
        self.assertFalse(pila2.has_setenta())

    def test_add(self):
        """Add cards to the pila, and retrieve them"""
        pila = Pila()
        card1 = Card(4, 'basto')
        card2 = Card(6, 'basto')
        card3 = Card(6, 'oro')
        card4 = Card(1, 'espada')

        pila.add([card1, card2])
        current_cards = pila.get_cards()
        self.assertEqual(2, len(current_cards['basto']))
        self.assertEqual(0, len(current_cards['oro']))
        self.assertEqual(0, len(current_cards['espada']))
        self.assertEqual(0, len(current_cards['copa']))

        pila.add([card3, card4])
        current_cards = pila.get_cards()
        self.assertEqual(2, len(current_cards['basto']))
        self.assertEqual(1, len(current_cards['oro']))
        self.assertEqual(1, len(current_cards['espada']))
        self.assertEqual(0, len(current_cards['copa']))

    def test_addEscoba(self):
        pila = Pila()
        self.assertEqual(0, pila.get_escobas())

        card1 = Card(7, 'oro')
        card2 = Card(8, 'copa')
        pila.add([card1, card2], True)

        self.assertEqual(1, pila.get_escobas())

    def test_get_cards(self):
        """.get_cards() returns a copy of the dictionary"""
        pila = Pila()
        card1 = Card(9, 'basto')
        card2 = Card(6, 'basto')
        card3 = Card(5, 'basto')
        pila.add([card1, card2])
        cards = pila.get_cards()
        # modifying the dictionary doesn't actually affect the pila
        cards['basto'].append(card3)

        pilaCards = pila.get_cards()
        self.assertEqual(2, len(pilaCards['basto']))

    def test_total_cards(self):
        """Counts the total number of cards the player has picked up.Counts"""
        pila = Pila()
        self.assertEqual(0, pila.total_cards())

        card1 = Card(9, 'basto')
        card2 = Card(6, 'basto')
        card3 = Card(5, 'espada')
        card4 = Card(1, 'oro')
        card5 = Card(3, 'copa')
        card6 = Card(5, 'espada')
        pila.add([card1, card2])
        self.assertEqual(2, pila.total_cards())

        pila.add([card3])
        self.assertEqual(3, pila.total_cards())

        pila.add([card4, card5, card6])
        self.assertEqual(6, pila.total_cards())

    def test_total_oros(self):
        """Counts the total number of oros collected by the player"""
        pila = Pila()
        self.assertEqual(0, pila.total_oros())
        card1 = Card(9, 'basto')
        card2 = Card(5, 'espada')
        card3 = Card(1, 'oro')
        card4 = Card(10, 'oro')
        card5 = Card(10, 'copa')
        pila.add([card1, card2])
        self.assertEqual(0, pila.total_oros())

        pila.add([card3])
        self.assertEqual(1, pila.total_oros())

        pila.add([card4, card5])
        self.assertEqual(2, pila.total_oros())

    def test_has_siete_de_belo(self):
        """Checks whether the 7 de belo is in the pile"""
        pila = Pila()
        card1 = Card(9, 'basto')
        card2 = Card(5, 'espada')
        card3 = Card(1, 'oro')
        card4 = Card(7, 'oro')
        card5 = Card(8, 'oro')
        card6 = Card(7, 'espada')

        pila.add([card1, card2, card3])
        self.assertFalse(pila.has_siete_de_belo())

        pila.add([card4])
        self.assertTrue(pila.has_siete_de_belo())

        pila.add([card5, card6])
        self.assertTrue(pila.has_siete_de_belo())

if __name__ == '__main__':
    unittest.main()