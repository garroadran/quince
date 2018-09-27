"""
The primary frame containing the content for the entire game
"""
import tkinter as tk
import time as time
import random as random
from ui.components.opponents.opponent_frame import OpponentFrameHorizontal, OpponentFrameVertical
from ui.components.table.table import Table
from ui.components.player.player_frame import PlayerFrame
from quince.ronda import Ronda


class GameFrame(tk.Frame):
    """Tk frame containing the main gameplay display including
    cards, decks, and avatars."""
    def __init__(self, parent, player, npc1, npc2, npc3):
        """Instantiate a new GameFrame

        Args:
            parent (Tk widget)
            player - Player object representing the (human) user
            npc1 (NPC) - Shadow player (opponent)
            npc2 (NPC) - Shadow player (opponent)
            npc3 (NPC) - Shadow player (opponent)
        """
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        self.npc1 = npc1
        self.npc2 = npc2
        self.npc3 = npc3
        self.player = player
        self.selected_table_cards = []

        self.ronda = Ronda.start([self.player, self.npc2, self.npc3, self.npc1], self.npc2)

    def draw(self):
        for widget in self.winfo_children():
            widget.destroy()

        myhand = self.ronda.player_cards[self.player]['hand']

        table_cards = self.ronda.current_mesa
        current_player = self.ronda.current_player

        # OPPONENT 1
        opp1_hand_size = len(self.ronda.player_cards[self.npc1]['hand'])
        opp1_active = current_player == self.npc1
        opp1 = OpponentFrameVertical(self, self.npc1.image(), self.npc1.name(), opp1_active, opp1_hand_size)
        opp1.grid(row=1, column=0)

        # OPPONENT 2
        opp2_active = current_player == self.npc2
        opp2_hand_size = len(self.ronda.player_cards[self.npc2]['hand'])
        opp2 = OpponentFrameHorizontal(self, self.npc2.image(), self.npc2.name(), opp2_active, opp2_hand_size)
        opp2.grid(row=0, column=1)

        # OPPONENT 3
        opp3_active = current_player == self.npc3
        opp3_hand_size = len(self.ronda.player_cards[self.npc3]['hand'])
        opp3 = OpponentFrameVertical(self, self.npc3.image(), self.npc3.name(), opp3_active, opp3_hand_size)
        opp3.grid(row=1, column=2)

        # PLAYER
        hud = PlayerFrame(self, myhand, self.play_hand)
        hud.grid(row=2, column=0, columnspan=3)

        # TABLE
        tbl = Table(self, table_cards, self.register_table_card_selection)
        tbl.grid(row=1, column=1)

    def register_table_card_selection(self, cards):
        self.selected_table_cards = cards

    def play_hand(self, hand_card):
        """Callback function executed when player clicks the "Play Hand" button.
        """
        if self.ronda.current_player.name() == 'Tina':
            print(f'Playing {hand_card} and picking up: {self.selected_table_cards}')
            self.ronda = self.ronda.play_turn(hand_card, self.selected_table_cards)
            self.draw()
            self.play_next_move()
        else:
            print("not your turn")

    def play_next_move(self):
        """Play a card from the hand
        """
        table_cards = self.ronda.current_mesa
        current_player = self.ronda.current_player

        if current_player.name() == 'Tina':
            pass
        else:
            sleep_time = random.randrange(1, 6)
            time.sleep(sleep_time)
            CUR_PLAYER_HAND = self.ronda.player_cards[current_player]['hand']
            (OWN_CARD, MESA_CARDS) = self.ronda.current_player.get_move(CUR_PLAYER_HAND, table_cards)

            self.ronda = self.ronda.play_turn(OWN_CARD, MESA_CARDS)
            print(f'CPU played: {OWN_CARD} -- {MESA_CARDS}')
            self.draw()
            self.play_next_move()
