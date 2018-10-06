import unittest
from quince.components import Card


class TestCard(unittest.TestCase):
    def test_info(self):
        """Returns a tuple containing suit and number"""
        c = Card(4, "basto")
        self.assertEqual((4, "basto"), c.info())

        # Check that an error is raised on an invalid number
        with self.assertRaises(ValueError):
            c = Card(13, "espada")

    def test_clone(self):
        """Clones a card"""
        c = Card(1, "oro")
        d = c.clone()

        # Modifying this private attribute just for the purposes of testing
        c.number = 3
        self.assertEqual((1, "oro"), d.info())

    def test_image(self):
        """Returns an image for the card"""
        card = Card(10, "oro")
        img = card.image()
        self.assertEqual("PNG", img.format)

    def test_points_setenta(self):
        """The number of points a card is worth in the setenta"""
        c = Card(7, "oro")
        self.assertTrue(10, c.points_setenta)

    def test_str(self):
        """String representation"""
        c = Card(1, "oro")
        s = str(c)
        self.assertTrue("1" in s)
        self.assertTrue("oro" in s)

    def test_repr(self):
        """String representation"""
        c = Card(1, "oro")
        s = repr(c)
        self.assertTrue("1" in s)
        self.assertTrue("oro" in s)
