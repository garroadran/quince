"""A ronda represents one play through a deck of cards.
Four cards are dealt on the table, and three to each player.
The players take turn playing their cards one at a time, until
they all exhaust the cards they have in hand. At that point,
they all get dealt three more cards from the deck each.

This repeats until the deck is empty.

Once a ronda is finished, the points for that ronda
can be calculated.
"""

# Ronda class depends on exceptions, so exceptions must be imported first
from quince.ronda.ronda_exceptions import RondaFinishedError, RondaNotFinishedError
from quince.ronda.ronda import Ronda