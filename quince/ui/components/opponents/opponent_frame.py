"""
Classes used to display the status of an opponent on the game board.
"""
import tkinter as tk
from quince.ui.components.common.avatar import PlayerAvatar
from quince.ui.components.opponents.hand import OpponentHand


class OpponentFrameBase(tk.Frame):
    """
        A frame containing all the elements necessary to visualize
        the opponent's status (how many cards they are holding,
        how many points they currently have, their name, etc.)
    """
    def __init__(self, parent, avatar_image, player_name, is_active, hand_size):
        tk.Frame.__init__(self, parent)

        self.hand = OpponentHand(self, hand_size)
        self.avatar = PlayerAvatar(self, avatar_image, player_name, is_active)

        self._place_elements()

    def refresh(self, hand_size, is_active):
        """Refreshes the child widgets with the updated parameters.

        Args:
            hand_size (int) Integer between 0 and 3
            is_active (bool) Whether or not it is currently this player's turn
        """
        self.hand.refresh(hand_size)
        self.avatar.refresh(is_active)

    def _place_elements(self):
        raise NotImplementedError("Subclasses must override this method.")


class OpponentFrameVertical(OpponentFrameBase):
    """
        Frame containing an opponent's avatar image directly above their cards.
    """
    def _place_elements(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.avatar.grid(row=0, column=0)
        self.hand.grid(row=1, column=0)


class OpponentFrameHorizontal(OpponentFrameBase):
    """
        Frame containing an opponent's avatar image to the left of their cards.
    """
    def _place_elements(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.avatar.grid(row=0, column=0)
        self.hand.grid(row=0, column=1)
