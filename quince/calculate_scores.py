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


def calculate_scores(players):
    """Compare all players' pilas and tally scores.

    Single points are awarded for:
    - Most cards
    - Most oros
    - Best Setenta score
    - 7 de velo
    - Each escoba

    This method returns the scores, but does not award them.

    Args:
        players - List of Player

    Returns:
        Dictionary containing records for each of the 5 types of scores.
        'most_cards' is a tuple ([players who tied for 1st place], card_count)
        'most_oros' is a tuple ([players who tied for 1st place], card_count)
        'setenta' is a tuple ([players who tied for 1st place], setenta_score)
        '7_de_velo' is a reference to the player who obtained the 7
        'escobas' is a list of tuples (player, escobas_count)
    """
    most_cards = PointsCounter()
    most_oros = PointsCounter()
    setenta = PointsCounter()

    ronda_points = {
        'escobas': []
    }

    for player in players:
        pila = player.pila()
        most_cards.compare(player, pila.total_cards())

        most_oros.compare(player, pila.total_oros())

        # This method is not yet implemented
        # setenta.compare(player, player.pila.setenta)

        if pila.has_siete_de_velo():
            ronda_points['7_de_velo'] = player

        escobas = pila.get_escobas()
        if escobas > 0:
            ronda_points['escobas'].append((player, escobas))

    ronda_points['most_cards'] = (most_cards.winners, most_cards.top_score)
    ronda_points['most_oros'] = (most_oros.winners, most_oros.top_score)
    ronda_points['setenta'] = (setenta.winners, setenta.top_score)

    return ronda_points
