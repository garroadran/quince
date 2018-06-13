import unittest, random
from quince.components import Deck, Player, Card, Pila
from quince.ronda import Ronda

class TestRonda(unittest.TestCase):
    def test_instantiate(self):
        alice = Player('Alice')
        bob = Player('bob')
        
        deck = Deck(Card)

        player_cards = {
            alice: { 'hand': [], 'pila': Pila()},
            bob: { 'hand': [], 'pila': Pila()},
        }
        
        ronda = Ronda(**{
            'current_player': bob,
            'dealer': alice,
            'deck': deck,
            'last_pickup': bob,
            'mesa': [],
            'players': [alice, bob],
            'player_cards': player_cards
        })
        
        self.assertTrue(isinstance(ronda, Ronda))


    def test_start(self):
        random.seed(0)

        alice = Player('Alice')
        bob = Player('Bob')
        ronda = Ronda.start([alice, bob], alice)
        self.assertTrue(isinstance(ronda, Ronda))
        
        # Alice deals, Bob plays first
        self.assertEqual(alice, ronda._dealer)
        self.assertEqual(bob, ronda.current_player)
        
        # Each player has three cards
        for val in ronda._player_cards.values():
            self.assertEqual(3, len(val['hand']))
        
        # The table has four cards
        self.assertEqual(4, len(ronda.current_mesa))


    def test_start_with_escoba(self):
        random.seed(27)
        
        alice = Player('Alice')
        bob = Player('Bob')
        ronda = Ronda.start([alice, bob], alice)
        self.assertFalse(ronda.current_mesa)
        
        alice_pila = ronda._player_cards[alice]['pila']
        self.assertEqual(4, alice_pila.total_cards())


    def test_play_turn(self):
        random.seed(0)

        alice = Player('Alice')
        bob = Player('Bob')
        ronda = Ronda.start([alice, bob], alice)
        # bob holds: [(6, 'basto'), (8, 'basto'), (4, 'copa')]
        # alice holds: [(1, 'oro'), (7, 'copa'), (4, 'oro')]
        # on table: [(10, 'espada'), (9, 'espada'), (1, 'basto'), (6, 'oro')]
        
        # bob drops a card
        ronda2 = ronda.play_turn(Card(8, 'basto'))
        self.assertTrue(Card(8, 'basto') in ronda._player_cards[bob]['hand'])
        self.assertTrue(Card(8, 'basto') not in ronda2._player_cards[bob]['hand'])


    def test_play_turn2(self):
        random.seed(0)

        alice = Player('Alice')
        bob = Player('Bob')
        ronda = Ronda.start([alice, bob], alice)
        # bob holds: [(6, 'basto'), (8, 'basto'), (4, 'copa')]
        # alice holds: [(1, 'oro'), (7, 'copa'), (4, 'oro')]
        # on table: [(10, 'espada'), (9, 'espada'), (1, 'basto'), (6, 'oro')]
        
        # bob picks up a card
        ronda2 = ronda.play_turn(Card(6, 'basto'), [Card(9, 'espada')])
        self.assertTrue(Card(6, 'basto') in ronda._player_cards[bob]['hand'])
        self.assertTrue(Card(6, 'basto') not in ronda2._player_cards[bob]['hand'])
        self.assertTrue(Card(9, 'espada') not in ronda2.current_mesa)


    def test_hand_is_done(self):
        alice = Player('alice')
        bob = Player('Bob')
        ronda = Ronda.start([alice, bob], alice)
        self.assertFalse(ronda._hand_is_done)
        
        ronda._player_cards[bob]['hand'] = []
        self.assertFalse(ronda._hand_is_done)

        ronda._player_cards[alice]['hand'] = []
        self.assertTrue(ronda._hand_is_done)


    def test_is_finished(self):
        alice = Player('Alice')
        bob = Player('bob')
        
        deck = Deck(Card).deal(40)[0]

        player_cards = {
            alice: { 'hand': [], 'pila': Pila()},
            bob: { 'hand': [], 'pila': Pila()},
        }
        
        ronda = Ronda(**{
            'current_player': bob,
            'dealer': alice,
            'deck': deck,
            'last_pickup': bob,
            'mesa': [],
            'players': [alice, bob],
            'player_cards': player_cards
        })
        
        self.assertTrue(ronda.is_finished)