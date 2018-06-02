import unittest
from quince.cpu import enumerate_possibilities
from quince.components import Card

class TestCPU(unittest.TestCase):
    def test_enumerate_possibilities(self):
        ace = Card(1, 'oro')
        tres = Card(3, 'oro')
        cinco = Card(5, 'oro')
        seis = Card(6, 'espada')
        siete_velo = Card(7, 'oro')
        sota_oro = Card(8, 'oro')
        sota_copa = Card(8, 'copa')
        caballo = Card(9, 'basto')

        empty_mesa = enumerate_possibilities([], [ace, cinco, tres])
        self.assertEqual([], empty_mesa)

        siete_sota = enumerate_possibilities([sota_oro, cinco, sota_copa], [siete_velo])
        self.assertTrue((siete_velo, sota_oro) in siete_sota)
        self.assertTrue((siete_velo, sota_copa) in siete_sota)
        self.assertFalse((siete_velo, cinco) in siete_sota)

        complicated_options = enumerate_possibilities([sota_oro, tres, cinco, caballo, ace], [siete_velo, seis])
        self.assertTrue((siete_velo, sota_oro) in complicated_options)
        self.assertTrue((seis, caballo) in complicated_options)
        self.assertTrue((seis, sota_oro, ace) in complicated_options)
        self.assertTrue((seis, tres, cinco, ace) in complicated_options)
