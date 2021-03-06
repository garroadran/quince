import unittest
from quince.components import Card


class TestCard(unittest.TestCase):
    def test_info(self):
        """Returns a tuple containing suit and value"""
        c = Card(4, "basto")
        self.assertEqual(4, c.value)
        self.assertEqual("basto", c.suit)

        # Check that an error is raised on an invalid value
        with self.assertRaises(ValueError):
            c = Card(13, "espada")

    def test_clone(self):
        """Clones a card"""
        c = Card(1, "oro")
        d = c.clone()

        c.value = 3
        self.assertEqual(1, d.value)
        self.assertEqual("oro", d.suit)

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
