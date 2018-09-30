"""
Frame containing the display where the user can see their own
cards and avatar.
"""

import tkinter as tk
from quince.ui.components.player.hand import PlayerHand
from quince.ui.components.common.avatar import PlayerAvatar


class PlayerFrame(tk.Frame):
    """
    Represents the HUD for the player's current hand, score, avatar, etc.
    """
    def __init__(self, parent, player, cards, is_active, callback):
        """
        Args:
            parent (Tk widget) - Root node for this frame
            player (Player) -
            cards (list of Card) - Cards currently in the player's hand
            is_active (bool) - True if it is this player's turn to move
            callback (function) - Command to execute when the user
            has selected what cards they want to play/pick up
        """
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        self.callback = callback

        self.avatar = PlayerAvatar(self,
                                   player.image(),
                                   player.name(),
                                   is_active)
        self.avatar.grid(row=0, column=0)

        self.p_hand = PlayerHand(self, cards)

        self.play_hand_btn = tk.Button(self,
                                       text="Play Hand",
                                       command=self.play_hand)
        self.play_hand_btn.grid(row=0, column=2)

        self.refresh(cards, is_active)

    def play_hand(self):
        """Wraps the callback function, providing it the
        card that the player has selected from their hand
        as the first argument.
        """
        self.callback(self.p_hand.selected_card())

    def refresh(self, cards, is_active):
        """Redraws the cards in the player's hand,
        the marker showing if it is the player's turn,
        and enables/disables the "Play hand" button.

        Args:
            cards (List of Card) - Cards in the player's hand
            is_active (bool) - Is it currently this player's turn to play?
        """
        self.avatar.refresh(is_active)

        btn_state = 'normal' if is_active else 'disabled'
        self.play_hand_btn.config(state=btn_state)

        self.p_hand.destroy()
        self.p_hand = PlayerHand(self, cards)
        self.p_hand.grid(row=0, column=1)
