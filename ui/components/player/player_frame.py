import tkinter as tk
import os
from PIL import Image
from ui.components.player.hand import PlayerHand
from ui.components.common.avatar import PlayerAvatar

class PlayerFrame(tk.Frame):
    """
    Represents the HUD for the player's current hand, score, avatar, etc.
    """
    def __init__(self, parent, cards):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)


        # PLAYER AVATAR
        relpath = f'ui/assets/avatars/dana.png'
        image_path = os.path.join(os.getcwd(), relpath)
        avatar_img = Image.open(image_path)
        player_name = "Dana"
        is_active = False
        self.avatar = PlayerAvatar(self, avatar_img, player_name, is_active)
        self.avatar.grid(row=0, column=0)

        # PLAYER HAND
        # c1pth = f'quince/assets/img/card_oro_5.png'
        # c1fpth = os.path.join(os.getcwd(), c1pth)
        # c1_img = Image.open(c1fpth)
        # card1 = {'value': 5, 'suit': 'oro', 'image': c1_img}

        # c2pth = f'quince/assets/img/card_basto_10.png'
        # c2fpth = os.path.join(os.getcwd(), c2pth)
        # c2_img = Image.open(c2fpth)
        # card2 = {'value': 8, 'suit': 'basto', 'image': c2_img}

        # cards = [card1, card2]
        p_hand = PlayerHand(self, cards)
        p_hand.grid(row=0, column=1)

        self.play_hand_btn = tk.Button(self, text="Play Hand")
        self.play_hand_btn.grid(row=0, column=2)
