import unittest
import random
from quince.components import Deck, Player, Card
from quince.ronda import Ronda, RondaFinishedError

random.seed(0)

class MockDeck(Deck):
  def __init__(self):
    a = Card(5, 'copa')
    b = Card(8, 'basto')
    c = Card(1, 'copa')
    d = Card(7, 'espada')
    e = Card(1, 'oro')
    f = Card(7, 'basto')
    g = Card(8, 'espada')
    h = Card(4, 'oro')
    i = Card(2, 'basto')
    j = Card(3, 'oro')
    self._cards = [a, b, c, d, e, f, g, h, i, j]

  def deal(self, amount):
    todeal = self._cards[0:amount]
    self._cards = self._cards[amount:]
    return todeal

class MockDeckEscobaDeal(MockDeck):
  def __init__(self):
    a = Card(4, 'basto')
    b = Card(4, 'oro')
    c = Card(4, 'copa')
    d = Card(3, 'oro')
    e = Card(5, 'oro')
    f = Card(5, 'oro')
    g = Card(5, 'oro')
    h = Card(5, 'oro')
    i = Card(5, 'oro')
    j = Card(5, 'oro')
    self._cards = [a, b, c, d, e, f, g, h, i, j]

class TestRonda(unittest.TestCase):
    def test_initial_deal(self):
      deck = MockDeckEscobaDeal()
      alice = Player('Alice')
      bob = Player('Bob')

      # instantiates the ronda, dealing an instant 15
      # Alice takes the cards from the table, and scores an escoba
      ronda = Ronda([alice, bob], alice, deck)
      alice_pila = alice.pila()
      self.assertEqual(1, alice_pila.get_escobas())
      self.assertEqual(4, len(alice_pila.get_cards()))
      self.assertEqual([], ronda.current_mesa)

    def test_next_player(self):
      deck = Deck(Card)
      alice = Player('Alice')
      bob = Player('Bob')
      charlie = Player('Charlie')

      ronda = Ronda([alice, bob], alice, deck)
      # since alice is dealer, bob should start play
      self.assertEqual(bob, ronda.current_player)
      # should cycle back around to alice
      ronda._next_player()
      self.assertEqual(alice, ronda.current_player)

      # do the same thing with more players
      deck = Deck(Card)
      ronda = Ronda([alice, bob, charlie], charlie, deck)
      self.assertEqual(alice, ronda.current_player)
      ronda._next_player()
      ronda._next_player()
      self.assertEqual(charlie, ronda.current_player)

    def test_current_mesa(self):
      # Returns a list of cards
      deck = Deck(Card)
      alice = Player('Alice')
      bob = Player('Bob')
      ronda = Ronda([alice, bob], bob, deck)
      for card in ronda.current_mesa:
        self.assertTrue(isinstance(card, Card))

    def test_play_turn(self):
      deck = Deck(Card)
      alice = Player('Alice')
      bob = Player('Bob')
      ronda = Ronda([alice, bob], alice, deck)

      for _ in  range(0, 35):
        # Both players do nothing except lay down cards
        card_to_play = ronda.current_player.current_hand()[0]
        ronda.play_turn(card_to_play.info(), [])
      self.assertEqual(39, len(ronda.current_mesa))

      # When the last card is played, the ronda finishes
      card_to_play = ronda.current_player.current_hand()[0]
      ronda.play_turn(card_to_play.info(), [])
      self.assertTrue(ronda.is_finished)

      # Can't play any more turns once the ronda is finished
      with self.assertRaises(RondaFinishedError):
        ronda.play_turn(None, None)

    def test_play_turn2(self):
      deck = MockDeck()
      alice = Player('Alice')
      bob = Player('Bob')
      ronda = Ronda([alice, bob], alice, deck)

      # Pick up cards into a player's pila
      ronda.play_turn(bob.current_hand()[2].info(), [(5, 'copa'), (7, 'espada')])
      self.assertEqual(3, bob.pila().total_cards())
      self.assertEqual(2, len(bob.current_hand()))
      self.assertEqual(2, len(ronda.current_mesa))

      # lay down a card
      ronda.play_turn(alice.current_hand()[0].info(), [])
      self.assertEqual(0, alice.pila().total_cards())
      self.assertEqual(2, len(alice.current_hand()))
      self.assertEqual(3, len(ronda.current_mesa))

    def test_dealt_escoba(self):
      # Remember whether the initial mesa deal was an escoba or not
      deck = MockDeckEscobaDeal()
      alice = Player('Alice')
      bob = Player('Bob')
      ronda = Ronda([alice, bob], alice, deck)
      self.assertTrue(ronda.dealt_escoba)

      deck = MockDeck()
      alice = Player('Alice')
      bob = Player('Bob')
      ronda = Ronda([alice, bob], alice, deck)
      self.assertFalse(ronda.dealt_escoba)