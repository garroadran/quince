import unittest
from quince.components import Card, Player, NPC


class TestPlayer(unittest.TestCase):
    def test_id(self):
        """Initialize different players with different ids"""
        a = Player("Alice")
        b = Player("Alice")
        self.assertTrue(a.id + 1 == b.id)

    def test_name(self):
        """Getter for the player's name"""
        alice = Player("Alice")
        self.assertEqual("Alice", alice.name())

    def test_str(self):
        """String representation"""
        p = Player("Annie")
        s = str(p)
        self.assertTrue("Annie" in s)

    def test_repr(self):
        """String representation"""
        p = Player("Billy")
        s = repr(p)
        self.assertTrue("Billy" in s)


class TestNPC(unittest.TestCase):
    def test_get_move_single_choice(self):
        """Given a hand and a mesa,
        select which cards to play and what to pick up."""
        npc = NPC()
        a = Card(5, "oro")
        b = Card(10, "oro")
        hand = [a]
        mesa = [b]
        (from_hand, from_mesa) = npc.get_move(hand, mesa)
        self.assertEqual(a, from_hand)
        self.assertEqual([b], from_mesa)

    def test_get_move_no_choice(self):
        """Drop a card if there are no moves available."""
        npc = NPC()
        a = Card(1, "oro")
        b = Card(1, "basto")
        c = Card(9, "copa")
        d = Card(8, "espada")
        hand = [a]
        mesa = [b, c, d]
        (from_hand, from_mesa) = npc.get_move(hand, mesa)
        self.assertEqual(a, from_hand)
        self.assertFalse(from_mesa)
