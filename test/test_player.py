import unittest
from quince.components import Card, Player, NPC

class TestPlayer(unittest.TestCase):
    def test_id(self):
        """Initialize different players with different ids"""
        a = Player('Alice')
        b = Player('Alice')
        self.assertTrue(a.id + 1 == b.id)


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


    def test_award_points(self):
        p = Player('Alice')
        # Award 1 point by default
        p.award_points()
        self.assertEqual(1, p.total_score())

        p.award_points(4)
        self.assertEqual(5, p.total_score())


    def test_raise_not_holding_card(self):
        """Raise an error if the player tries to drop a card they don't have"""
        p = Player('Alice')
        with self.assertRaises(ValueError):
            p.place_card_on_mesa([], (4, 'copa'))


    def test_raise_various(self):
        """Raise errors if trying to perform illegal pickups"""
        p = Player('Alice')
        mesa = [Card(5, 'espada')]
        p.pick_up_hand([Card(8, 'copa'), Card(10, 'oro'), Card(8, 'espada')])
        with self.assertRaises(ValueError):
            p.pick_up_from_mesa(mesa, (8, 'copa'), [(5, 'espada')])

        with self.assertRaises(ValueError):
            p.pick_up_from_mesa(mesa, (3, 'copa'), [])

        with self.assertRaises(ValueError):
            p.pick_up_from_mesa(mesa, (8, 'copa'), [(7, 'oro')])

    def test_str(self):
        """String representation"""
        p = Player('Annie')
        s = str(p)
        self.assertTrue('Annie' in s)


    def test_repr(self):
        """String representation"""
        p = Player('Billy')
        s = repr(p)
        self.assertTrue('Billy' in s)


class TestNPC(unittest.TestCase):
    def test_get_move_single_choice(self):
        """Given a hand and a mesa, select which cards to play and what to pick up."""
        npc = NPC()
        a = Card(5, 'oro')
        b = Card(10, 'oro')
        hand = [a]
        mesa = [b]
        (from_hand, from_mesa) = npc.get_move(hand, mesa)
        self.assertEqual(a, from_hand)
        self.assertEqual([b], from_mesa)


    def test_get_move_no_choice(self):
        """Drop a card if there are no moves available."""
        npc = NPC()
        a = Card(1, 'oro')
        b = Card(1, 'basto')
        c = Card(9, 'copa')
        d = Card(8, 'espada')
        hand = [a]
        mesa = [b, c, d]
        (from_hand, from_mesa) = npc.get_move(hand, mesa)
        self.assertEqual(a, from_hand)
        self.assertFalse(from_mesa)
