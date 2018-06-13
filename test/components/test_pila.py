import unittest
from quince.components import Pila, Card

class TestPila(unittest.TestCase):
    def test_add(self):
        """Add cards to the pila, and retrieve them"""
        pila = Pila()
        card1 = Card(4, 'basto')
        card2 = Card(6, 'basto')
        card3 = Card(6, 'oro')
        card4 = Card(1, 'espada')

        pila2 = pila.add([card1, card2])
        current_cards = pila2.get_cards()
        self.assertEqual(2, len(current_cards['basto']))
        self.assertEqual(0, len(current_cards['oro']))
        self.assertEqual(0, len(current_cards['espada']))
        self.assertEqual(0, len(current_cards['copa']))

        pila3 = pila2.add([card3, card4])
        current_cards = pila3.get_cards()
        self.assertEqual(2, len(current_cards['basto']))
        self.assertEqual(1, len(current_cards['oro']))
        self.assertEqual(1, len(current_cards['espada']))
        self.assertEqual(0, len(current_cards['copa']))


    def test_add_does_not_modify(self):
        """Returns a new pila, and does not modify the existing one"""
        pila1 = Pila()
        card1 = Card(3, 'basto')
        pila2 = pila1.add([card1])
        self.assertEqual(0, pila1.total_cards())
        self.assertEqual(1, pila2.total_cards())


    def test_addEscoba(self):
        pila = Pila()
        self.assertEqual(0, pila.escobas)

        card1 = Card(7, 'oro')
        card2 = Card(8, 'copa')
        pila2 = pila.add([card1, card2], True)

        self.assertEqual(1, pila2.escobas)


    def test_get_cards(self):
        """.get_cards() returns a copy of the dictionary"""
        pila = Pila()
        card1 = Card(9, 'basto')
        card2 = Card(6, 'basto')
        card3 = Card(5, 'basto')
        pila2 = pila.add([card1, card2])
        cards = pila2.get_cards()
        # modifying the dictionary doesn't actually affect the pila
        cards['basto'].append(card3)

        pilaCards = pila2.get_cards()
        self.assertEqual(2, len(pilaCards['basto']))


    def test_total_cards(self):
        """Counts the total number of cards the player has picked up."""
        pila = Pila()
        self.assertEqual(0, pila.total_cards())

        card1 = Card(9, 'basto')
        card2 = Card(6, 'basto')
        card3 = Card(5, 'espada')
        card4 = Card(1, 'oro')
        card5 = Card(3, 'copa')
        card6 = Card(5, 'espada')
        pila2 = pila.add([card1, card2])
        self.assertEqual(2, pila2.total_cards())

        pila3 = pila2.add([card3])
        self.assertEqual(3, pila3.total_cards())

        pila4 = pila3.add([card4, card5, card6])
        self.assertEqual(6, pila4.total_cards())


    def test_total_oros(self):
        """Counts the total number of oros collected by the player"""
        pila = Pila()
        self.assertEqual(0, pila.total_oros())
        card1 = Card(9, 'basto')
        card2 = Card(5, 'espada')
        card3 = Card(1, 'oro')
        card4 = Card(10, 'oro')
        card5 = Card(10, 'copa')
        pila2 = pila.add([card1, card2])
        self.assertEqual(0, pila2.total_oros())

        pila3 = pila2.add([card3])
        self.assertEqual(1, pila3.total_oros())

        pila4 = pila3.add([card4, card5])
        self.assertEqual(2, pila4.total_oros())


    def test_has_siete_de_velo(self):
        """Checks whether the 7 de velo is in the pile"""
        pila = Pila()
        card1 = Card(9, 'basto')
        card2 = Card(5, 'espada')
        card3 = Card(1, 'oro')
        card4 = Card(7, 'oro')
        card5 = Card(8, 'oro')
        card6 = Card(7, 'espada')

        pila2 = pila.add([card1, card2, card3])
        self.assertFalse(pila2.has_siete_de_velo())

        pila3 = pila2.add([card4])
        self.assertTrue(pila3.has_siete_de_velo())

        pila4 = pila3.add([card5, card6])
        self.assertTrue(pila4.has_siete_de_velo())


    def test_best_setenta(self):
        basto4 = Card(4, 'basto')
        oro7 = Card(7, 'oro')
        espada10 = Card(10, 'espada')
        copa1 = Card(1, 'copa')
        copa5 = Card(5, 'copa')

        # Only one option
        pila1 = Pila()
        pila2 = pila1.add([basto4, oro7, espada10, copa1])
        setenta = [x.info() for x in pila2.best_setenta()]
        self.assertTrue(basto4.info() in setenta)
        self.assertTrue(oro7.info() in setenta)
        self.assertTrue(espada10.info() in setenta)
        self.assertTrue(copa1.info() in setenta)

        # No setenta possible
        pila = Pila()
        pila2 = pila.add([oro7, espada10, copa1, copa5])
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
        pila2 = pila1.add([basto4, oro7, espada10, copa5, copa1])
        setenta = [x.info() for x in pila2.best_setenta()]
        self.assertTrue(copa1.info() in setenta)
        
        pila1 = Pila()
        pila2 = pila1.add([copa5, basto4, oro4, espada10, oro7, copa1])
        setenta = [x.info() for x in pila2.best_setenta()]
        self.assertTrue(copa1.info() in setenta)
        self.assertTrue(oro7.info() in setenta)


    def test_reset(self):
        """Reset a pila to an empty state.
        This method can probably be removed"""
        a = Card(1, 'oro')
        b = Card(2, 'oro')
        p = Pila()
        p2 = p.add([a, b])
        self.assertEqual(2, p2.total_cards())
        p3 = p2.reset()
        self.assertEqual(0, p3.total_cards())
        