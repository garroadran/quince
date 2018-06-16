"""
Integral components of the game.

Card - A base class describing cards. Derived classes might differ,
for example, in the way images are generated.

Deck - A deck of cards. Supports dealing cards at random.

Pila - Represents the collection of cards that a player piles up
as they collect cards on their turns.

Player - A player of the game.
"""

__all__ = ['Card', 'Deck', 'Pila', 'Player', 'NPC']

from quince.components.card import Card
from quince.components.deck import Deck
from quince.components.pila import Pila
from quince.components.player import Player, NPC
