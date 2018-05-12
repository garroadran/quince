"""
Integral components of the game.

Card - A base class describing cards. Derived classes might differ,
for example, in the way images are generated.

Deck - A deck of cards. Supports dealing cards at random.

Pila - Represents the collection of cards that a player piles up
as they collect cards on their turns.

Player - A player of the game.
"""

from quince.components.Card import Card
from quince.components.Deck import Deck
from quince.components.Pila import Pila
from quince.components.Player import Player
