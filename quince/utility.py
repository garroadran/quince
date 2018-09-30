def is_valid_pickup(player_card, mesa_cards):
    """Determines whether a move is valid.

    Args:
        player_card (Card) - The card that a player puts
        down from their hand
        mesa_cards (List of Card) - The cards that the
        player picks up from the table
    """
    total_sum = player_card.number + sum([x.number for x in mesa_cards])

    # Any single card can be dropped
    if total_sum == 15 or not mesa_cards:
        return True

    return False


class GridPosition(object):
    """Specifies a zero-indexed, two-dimensional coordinate point.
    """
    def __init__(self, column_count):
        """Instantiates a GridPosition object with column_count columns.

        Args:
            column_count (int) - Positive integer
        """
        if column_count < 0:
            raise AttributeError("Cannot have a negative amount of columns")

        self.column_count = column_count
        self.row = 0
        self.column = 0

    def get_value(self):
        """Getter for the current position. Returns a tuple of (row, column)
        """
        return self.row, self.column

    def increment_right(self):
        """Moves one position over to the right. If the last column is reached,
        wraps around to the next row.

        Returns:
            A tuple indicating the current position, after the increment (row, column)
        """
        if self.column == self.column_count - 1:
            self.column = 0
            self.row += 1
        else:
            self.column += 1

        return self.get_value()
