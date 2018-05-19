"""
This file contains an extremely crude and simplified CLI interface for playing a ronda.

Run this function from the command line.
In the root directory, run `python -m quince.rondarunner`
"""

from ast import literal_eval
from quince.components import Player, Card, Deck
from quince.ronda import Ronda

def get_mesa_cards(empty_mesa=False):
    """Prompt the user to select which cards from the mesa they would like to pick up.
    """
    if empty_mesa:
        print(">>> Mesa is empty. Dropping cards.")
        return []

    while True:
        try:
            usr_input = input('What cards would you like to pick up? ' +
                              '(array of integers, or "drop" to drop): ')
            if usr_input != 'drop' and usr_input != '':
                mesa_card_choices = literal_eval(usr_input)
                mesa_cards = [MESA[i-1].info() for i in mesa_card_choices]
            else:
                mesa_cards = []
                print(">>> Dropped card on the table")
            return mesa_cards
        except (ValueError, IndexError):
            print('Invalid entry.')

ALICE = Player('Alice')
BOB = Player('Bob')
CHARLIE = Player('Charlie')
DAVE = Player('Dave')

RONDA = Ronda([ALICE, BOB, CHARLIE, DAVE], BOB, Deck(Card))

print('///////////////////////////')
print('     Dealing cards . . .')
print('///////////////////////////')

while not RONDA.is_finished():

    # Display the current status
    print(RONDA.current_player().name() + ' holds the following cards:')
    HAND = RONDA.current_player().current_hand()
    for i in range(1, len(HAND) + 1):
        print('>>> ' + str(i) + ': ' + str(HAND[i-1].info()))
    print('')
    print('The cards on the mesa are:')
    MESA = RONDA.current_mesa()
    for i in range(1, len(MESA) + 1):
        print('>>> ' + str(i) + ': ' + str(MESA[i-1].info()))
    print('...')

    # Play a card from the hand
    while True:
        CARD_CHOICE = int(input('what card will ' + RONDA.current_player().name() +
                                ' play? (integer): '))
        try:
            OWN_CARD = HAND[CARD_CHOICE - 1].info()
            break
        except (ValueError, IndexError):
            print('Invalid entry.')
    print(RONDA.current_player().name() + ' plays a ' + str(OWN_CARD))

    # select cards from mesa
    while True:
        try:
            MESA_CARDS = get_mesa_cards(RONDA.current_mesa() == [])
            RONDA.play_turn(OWN_CARD, MESA_CARDS)
            break
        except ValueError:
            print('Invalid entry.')
    print('.')
    print('.')
    print('.')

    if RONDA.current_player() == BOB and len(BOB.current_hand()) == 3:
        print('///////////////////////////')
        print('     Dealing cards . . .')
        print('///////////////////////////')

print('Ronda finished!')
