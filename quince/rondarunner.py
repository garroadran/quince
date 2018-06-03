"""
This file contains an extremely crude and simplified CLI interface for playing a ronda.

Run this function from the command line.
In the root directory, run `python -m quince.rondarunner`
"""

from ast import literal_eval
import random
from quince.components import Player, Card, Deck, NPC
from quince.ronda import Ronda
from quince.calculate_scores import calculate_scores

random.seed(0)

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


def getchoices(current_hand, current_mesa):
    """Get card choices via CLI"""
    own_card = None
    mesa_cards = []
    while True:
        card_choice = int(input('what card will you play? (integer): '))
        try:
            own_card = current_hand[card_choice - 1].info()
            break
        except (ValueError, IndexError):
            print('Invalid entry.')

    # select cards from mesa
    while True:
        try:
            mesa_cards = get_mesa_cards(current_mesa == [])
            break
        except ValueError:
            print('Invalid entry.')

    return (own_card, mesa_cards)


ALICE = Player('Alice')
BOB = NPC('Bob')
CHARLIE = NPC('Charlie')
DAVE = NPC('Dave')

RONDA = Ronda([ALICE, BOB, CHARLIE, DAVE], BOB, Deck(Card))

print('///////////////////////////')
print('     Dealing cards . . .')
print('///////////////////////////')

while not RONDA.is_finished:

    # Display the current status
    PLAYER = RONDA.current_player
    PLAYERNAME = PLAYER.name()
    print(PLAYERNAME + ' holds the following cards:')
    HAND = RONDA.current_player.current_hand()
    for i in range(1, len(HAND) + 1):
        print('>>> ' + str(i) + ': ' + str(HAND[i-1].info()))
    print('')
    print('The cards on the mesa are:')
    MESA = RONDA.current_mesa
    for i in range(1, len(MESA) + 1):
        print('>>> ' + str(i) + ': ' + str(MESA[i-1].info()))
    print('...')

    # Play a card from the hand
    if PLAYERNAME == 'Alice':
        (OWN_CARD, MESA_CARDS) = getchoices(HAND, RONDA.current_mesa)
    else:
        CUR_PLAYER_HAND = PLAYER.current_hand()
        (OWN_CARD, MESA_CARDS) = PLAYER.get_move(CUR_PLAYER_HAND, MESA)
        OWN_CARD = OWN_CARD.info()
        MESA_CARDS = [x.info() for x in MESA_CARDS]

    if MESA_CARDS:
        MSG = PLAYERNAME + ' plays a ' + str(OWN_CARD) + ' and picks up ' + str(MESA_CARDS)
    else:
        MSG = PLAYERNAME + ' drops a ' + str(OWN_CARD)

    print(MSG)

    RONDA.play_turn(OWN_CARD, MESA_CARDS)
    print('.')

    if RONDA.current_player == CHARLIE and len(CHARLIE.current_hand()) == 3:
        print('///////////////////////////')
        print('     Dealing cards . . .')
        print('///////////////////////////')

print('Ronda finished!')
print('')

SCORES = calculate_scores([ALICE, BOB, CHARLIE, DAVE])

print('-------PUNTUAJE----------')
for key in SCORES:
    print(key + ':\t' + str(SCORES[key]))
