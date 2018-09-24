"""
Shows an avatar and name for a player.
"""
import tkinter as tk
from PIL import Image, ImageTk


class PlayerAvatar(tk.Frame):
    """
    The player's avatar and name.
    A highlight is shown if it is the player's turn.
    """
    def __init__(self, parent, image, player_name="Player Name", isActive=False):
        """
        Args:
            parent (tk.Frame) - The root node where this frame is packed
            image (PIL.Image) - Image for the player (1x1 ratio)
            player_name (string)
            isActive (bool) - Whether or not it is currently this player's turn
        """
        tk.Frame.__init__(self, parent)

        # row expands as the window grows
        self.grid_rowconfigure(0, weight=1)

        # col 0 doesn't expand, col 1 does
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)


        resized = image.resize((75, 75), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)

        img_args = { 'image': img }

        if isActive:
            img_args['background'] = 'red'

        img_label = tk.Label(self, **img_args)
        img_label.image = img # hold on to the reference

        label = tk.Label(self, text=player_name)

        img_label.grid(row=0, column=0)
        label.grid(row=0, column=1, sticky="nw", padx=10)
