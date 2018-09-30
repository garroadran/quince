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
    def __init__(self,
                 parent,
                 image,
                 player_name="Player Name",
                 is_active=False):
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

        image.thumbnail((65, 65), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)

        self.img_label = tk.Label(self, image=img, relief='solid')
        self.img_label.image = img  # hold on to the reference

        self.label = tk.Label(self, text=player_name)

        self.img_label.grid(row=0, column=0)
        self.label.grid(row=0, column=1, sticky="nw", padx=10)

        self.refresh(is_active)

    def refresh(self, is_active):
        """Updates the avatar image to mark whether or not
        it is this player's turn to play.

        Args:
            is_active (bool) - Is it this player's turn to play?
        """
        width = 1 if is_active else 0
        self.img_label.config(borderwidth=width)
