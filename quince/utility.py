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
