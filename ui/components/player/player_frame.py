import tkinter as tk
import os
from PIL import Image
from ui.components.player.hand import PlayerHand
from ui.components.common.avatar import PlayerAvatar

class PlayerFrame(tk.Frame):
    """
    Represents the HUD for the player's current hand, score, avatar, etc.
    """
    def __init__(self, parent, cards, is_active, callback):
        """
        Args:
            parent (Tk widget) - Root node for this frame
            cards (list of Card) - Cards currently in the player's hand
            callback (function) - Command to execute when the user
            has selected what cards they want to play/pick up
        """
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        self.callback = callback

        # PLAYER AVATAR
        relpath = f'ui/assets/avatars/dana.png'
        image_path = os.path.join(os.getcwd(), relpath)
        avatar_img = Image.open(image_path)
        player_name = "Dana"
        self.avatar = PlayerAvatar(self, avatar_img, player_name, is_active)
        self.avatar.grid(row=0, column=0)

        # PLAYER HAND
        self.p_hand = PlayerHand(self, cards)
        self.p_hand.grid(row=0, column=1)

        btn_state = 'normal' if is_active else 'disabled'
        self.play_hand_btn = tk.Button(self, text="Play Hand", command=self.play_hand, state=btn_state)
        self.play_hand_btn.grid(row=0, column=2)

    def play_hand(self):
        """Wraps the callback function, providing it the
        card that the player has selected from their hand
        as the first argument.
        """
        self.callback(self.p_hand.selected_card())
