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


    def test_points_setenta(self):
        """The number of points a card is worth in the setenta"""
        c = Card(7, 'oro')
        self.assertTrue(10, c.points_setenta)


    def test_str(self):
        """String representation"""
        c = Card(1, 'oro')
        s = str(c)
        self.assertTrue('1' in s)
        self.assertTrue('oro' in s)


    def test_repr(self):
        """String representation"""
        c = Card(1, 'oro')
        s = repr(c)
        self.assertTrue('1' in s)
        self.assertTrue('oro' in s)

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


    def test_str(self):
        """String representation"""
        d = Deck(Card)
        s = str(d)
        self.assertTrue('40' in s)


    def test_repr(self):
        """String representation"""
        d = Deck(Card)
        d.deal(4)
        s = repr(d)
        self.assertTrue('36' in s)


class TestPila(unittest.TestCase):
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


    def test_has_siete_de_velo(self):
        """Checks whether the 7 de velo is in the pile"""
        pila = Pila()
        card1 = Card(9, 'basto')
        card2 = Card(5, 'espada')
        card3 = Card(1, 'oro')
        card4 = Card(7, 'oro')
        card5 = Card(8, 'oro')
        card6 = Card(7, 'espada')

        pila.add([card1, card2, card3])
        self.assertFalse(pila.has_siete_de_velo())

        pila.add([card4])
        self.assertTrue(pila.has_siete_de_velo())

        pila.add([card5, card6])
        self.assertTrue(pila.has_siete_de_velo())


    def test_best_setenta(self):
        basto4 = Card(4, 'basto')
        oro7 = Card(7, 'oro')
        espada10 = Card(10, 'espada')
        copa1 = Card(1, 'copa')
        copa5 = Card(5, 'copa')

        # Only one option
        pila1 = Pila()
        pila1.add([basto4, oro7, espada10, copa1])
        setenta = [x.info() for x in pila1.best_setenta()]
        self.assertTrue(basto4.info() in setenta)
        self.assertTrue(oro7.info() in setenta)
        self.assertTrue(espada10.info() in setenta)
        self.assertTrue(copa1.info() in setenta)

        # No setenta possible
        pila2 = Pila()
        pila2.add([oro7, espada10, copa1, copa5])
        setenta = pila2.best_setenta()
        self.assertFalse(setenta)


    def test_best_setenta2(self):
        basto4 = Card(4, 'basto')
        oro7 = Card(7, 'oro')
        oro4 = Card(4, 'oro')
        espada10 = Card(10, 'espada')
        copa1 = Card(1, 'copa')
        copa5 = Card(5, 'copa')

        pila1 = Pila()
        pila1.add([basto4, oro7, espada10, copa5, copa1])
        setenta = [x.info() for x in pila1.best_setenta()]
        self.assertTrue(copa1.info() in setenta)
        
        pila2 = Pila()
        pila2.add([copa5, basto4, oro4, espada10, oro7, copa1])
        setenta = [x.info() for x in pila2.best_setenta()]
        self.assertTrue(copa1.info() in setenta)
        self.assertTrue(oro7.info() in setenta)


    def test_reset(self):
        a = Card(1, 'oro')
        b = Card(2, 'oro')
        p = Pila()
        p.add([a, b])
        self.assertEqual(2, p.total_cards())
        p.reset()
        self.assertEqual(0, p.total_cards())


if __name__ == '__main__':
    unittest.main()