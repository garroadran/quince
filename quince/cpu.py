"""
Module containing CPU Player logic
"""


def enumerate_possibilities(mesa, hand):
    """Finds all the way of adding to 15 using exactly 1 card from the hand,
    and any arbitrary number from the mesa.

    Args:
         mesa -- List of Card objects
         hand -- List of Card objects

    Returns:
        List of tuples, each representing a different possibility for adding
        up to 15.
        Example: [(card1, card2), (card1, card3, card4)]

    Example:
        >>> from quince.components.card import Card
        >>> card1 = Card(1, "oro")
        >>> card2 = Card(9, "espada")
        >>> card3 = Card(2, "oro")
        >>> card4 = Card(4, "copa")
        >>> card5 = Card(3, "copa")
        >>> card6 = Card(2, "basto")
        >>> card7 = Card(5, "espada")

        >>> mesa = [card1, card2, card3, card4]
        >>> hand = [card5, card6, card7]

        >>> result = enumerate_possibilities(mesa, hand)
        >>> result == [(card5, card1, card2, card3), (card6, card2, card4),
        ...            (card7, card1, card2)]
        True
    """

    def find_permutation(card_pool, partial_sum, permutations):
        """Recursively find all permutations of card_pool and partial_sum
        which add to 15, and append each result to permutations
        """

        # calculate the current sum of all cards in partial_sum
        current_sum = sum([card.info()[0] for card in partial_sum])
        if current_sum == 15:
            # found a permutation, append it to permutations
            permutations.append(tuple(partial_sum))
        if current_sum >= 15:
            # at or beyond target sum, so stop recursing
            return

        # for each remaining card in card_pool, see if there is a permutation
        # adding to the target, given the current partial_sum
        for card in enumerate(card_pool):
            remaining_cards = card_pool[card[0] + 1:]
            new_partial_sum = partial_sum + [card[1]]
            find_permutation(remaining_cards, new_partial_sum, permutations)

    permutations = []
    # for each card in the hand, find all permutations that add to 15
    for card in hand:
        find_permutation(mesa, [card], permutations)
    return permutations
