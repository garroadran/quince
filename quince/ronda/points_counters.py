"""
Methods for use in calculating the scores after a single complete ronda.
"""

class PointsCounter(object):
    """An abstraction for keeping track of who has the highest score in
    any one particular score type.

    If two or more players tie for a particular score type, both will
    receive a point.
    """
    def __init__(self):
        """Constructor for the counter object.
        Creates a players list to track which players have the current highest score
        and an attribute to track the best score seen so far.
        """
        self._players = []
        self.top_score = 0


    @property
    def winners(self):
        """Getter for the players who are tied for the top score.
        """
        return self._players


    def compare(self, player, score):
        """Evaluates a score, and decides whether it is the top point-getter or not.
        Players that are tied for the top score will all earn points for that score
        type.
        """
        if score == self.top_score:
            self._players.append(player)
        elif score > self.top_score:
            self._players = [player]
            self.top_score = score


class SetentaCounter(PointsCounter):
    """Subclass of PointsCounter, with specific logic to calculate and generate setenta
    scores"""

    def compare(self, player, setenta_cards):
        """Identical to the base class's method, except it requires two extra
        steps in order to calculate the points for the given cards, and to create
        an object that will store the reference to the player, the cards, and the
        points.

        Args:
            player -- Reference to a player object
            setenta_cards -- List of Card objects used to make up a setenta.

        Returns:
            Nothing. Modifies the self._players and self.top_score attributes.
        """
        # must have a card of each suit to play the setenta
        if len(setenta_cards) < 4:
            return

        setenta_score = sum([card.points_setenta for card in setenta_cards])
        winner = SetentaWinner(player, setenta_cards)

        if setenta_score == self.top_score:
            self._players.append(winner)
        elif setenta_score > self.top_score:
            self._players = [winner]
            self.top_score = setenta_score


class SetentaWinner(object):
    """Describes the results for a player's setenta.
    Includes a reference to the player, the points for that setenta,
    and a list with references to the cards they used to make it up."""

    def __init__(self, player, cards):
        self.player = player
        self.cards = cards
        self.points = sum([card.points_setenta for card in cards])


    def __repr__(self):
        return f'{self.player} has {self.points} setenta pts.'


    def __str__(self):
        return f'{self.player} has {self.points} setenta pts.'
