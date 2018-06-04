import unittest
from quince.components import Card
from quince.calculate_scores import PointsCounter, SetentaWinner, calculate_scores


class MockPlayer(object):
    types = ['most_cards', 'most_oros', 'siete_de_velo', 'setenta']
    current_type = 0

    def __init__(self):
        if MockPlayer.current_type == 4:
            raise ValueError()

        self.type = MockPlayer.types[MockPlayer.current_type]
        MockPlayer.current_type += 1
        self._pila = MockPila(self.type)


    def pila(self):
        return self._pila


class MockPila(object):
    def __init__(self, type):
        self._total_cards = 8
        self._total_oros = 2
        self.has_siete = False
        self._escobas = 0
        self._setenta = []

        if type == 'most_cards':
            self._total_cards = 16
        elif type == 'most_oros':
            self._total_oros = 4
        elif type == 'siete_de_velo':
            self.has_siete = True
            self._setenta = [Card(3, 'oro'), Card(10, 'basto'), Card(5, 'espada'), Card(6, 'copa')]
        elif type == 'setenta':
            self._setenta = [Card(7, 'oro'), Card(7, 'basto'), Card(7, 'espada'), Card(7, 'copa')]
            self._escobas = 2


    def total_cards(self):
        return self._total_cards


    def total_oros(self):
        return self._total_oros


    def best_setenta(self):
        return self._setenta


    def get_escobas(self):
        return self._escobas


    def has_siete_de_velo(self):
        return self.has_siete


class TestPointsCounter(unittest.TestCase):
    def test_get_winner(self):
        counter = PointsCounter()
        counter.compare('dave', 6)
        counter.compare('bonnie', 6)
        self.assertTrue('dave' in counter.winners)
        self.assertTrue('bonnie' in counter.winners)


    def test_compare(self):
        counter = PointsCounter()
        counter.compare('annie', 6)
        counter.compare('bill', 4)
        self.assertTrue('annie' in counter.winners)
        self.assertTrue('bill' not in counter.winners)

        counter.compare('regina', 10)
        self.assertTrue('regina' in counter.winners)
        self.assertTrue('annie' not in counter.winners)

        counter.compare('cray', 10)
        self.assertTrue('cray' in counter.winners)
        self.assertTrue('regina' in counter.winners)


class TestSetentaWinner(unittest.TestCase):
    def test_instantiation(self):
        player = 'alice'
        winner = SetentaWinner(player, [])
        self.assertEqual('alice', winner.player)


class TestCalculateScores(unittest.TestCase):
    def test_calculate_scores(self):
        most_cards_player = MockPlayer()
        most_oros_player = MockPlayer()
        siete_player = MockPlayer()
        setenta_escobas_player = MockPlayer()

        scores = calculate_scores([most_cards_player, most_oros_player,
        siete_player, setenta_escobas_player])

        self.assertTrue(most_cards_player in scores['most_cards'][0])
        self.assertTrue(most_oros_player not in scores['most_cards'][0])
        self.assertEqual(16, scores['most_cards'][1])

        self.assertTrue(most_oros_player in scores['most_oros'][0])
        self.assertTrue(setenta_escobas_player not in scores['most_oros'][0])
        self.assertEqual(4, scores['most_oros'][1])

        self.assertTrue(scores['7_de_velo'] is siete_player)
        
        self.assertTrue(setenta_escobas_player in [x.player for x in scores['setenta']])
