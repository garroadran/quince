import unittest
from quince.components import Card
from quince.ronda import PointsCounter, SetentaCounter


class TestPointsCounter(unittest.TestCase):
    def test_compare(self):
        pc = PointsCounter()
        # Single player automatically becomes the top scorer
        pc.compare("alice", 10)
        self.assertTrue("alice" in pc.winners)

        # Tied scores are all winners
        pc.compare("bob", 10)
        self.assertTrue("alice" in pc.winners)
        self.assertTrue("bob" in pc.winners)

        # Bigger scores override all others
        pc.compare("charlie", 11)
        pc.compare("dave", 3)
        self.assertTrue("alice" not in pc.winners)
        self.assertTrue("bob" not in pc.winners)
        self.assertTrue("dave" not in pc.winners)
        self.assertTrue("charlie" in pc.winners)


class TestSetentaCounter(unittest.TestCase):
    def test_compare(self):
        pc = SetentaCounter()
        a_hand = [Card(5, "oro"), Card(6, "basto"),
                  Card(4, "espada"), Card(6, "copa")]
        b_hand = [Card(2, "oro"), Card(2, "basto"),
                  Card(5, "espada"), Card(2, "copa")]
        c_hand = [Card(6, "oro"), Card(1, "basto"),
                  Card(6, "espada"), Card(7, "copa")]

        pc.compare("alice", a_hand)
        self.assertTrue("alice" in [x.player for x in pc.winners])

        pc.compare("bob", b_hand)
        self.assertTrue("alice" in [x.player for x in pc.winners])
        self.assertTrue("bob" not in [x.player for x in pc.winners])

        pc.compare("charlie", c_hand)
        self.assertTrue("alice" not in [x.player for x in pc.winners])
        self.assertTrue("bob" not in [x.player for x in pc.winners])
        self.assertTrue("charlie" in [x.player for x in pc.winners])

    def test_four_suits_required(self):
        pc = SetentaCounter()
        a_hand = [Card(7, "oro"), Card(7, "basto"), Card(7, "espada")]
        b_hand = [Card(2, "oro"), Card(2, "basto"),
                  Card(2, "espada"), Card(2, "copa")]

        pc.compare("alice", a_hand)
        pc.compare("bob", b_hand)
        self.assertTrue("alice" not in [x.player for x in pc.winners])
        self.assertTrue("bob" in [x.player for x in pc.winners])
