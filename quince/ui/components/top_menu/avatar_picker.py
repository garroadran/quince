"""
A TopLevel tkinter widget that allows the user
to select an avatar image.
"""
import tkinter as tk
from os import scandir, getcwd
from os.path import join
from PIL import Image, ImageTk
from quince.utility import GridPosition


def get_files_from_dir(path):
    """Gets a list of the absolute paths of all the files in a
    specific directory. Does not traverse down the filetree"""
    return [f.path for f in scandir(path) if f.is_file]


class AvatarPicker(tk.Toplevel):
    """A window widget that the user can use to
    select an avatar image. The calling widget must
    provide a callback function so that this object
    can pass it the path to the new avatar.
    """
    def __init__(self, root, callback, *args, **kwargs):
        tk.Toplevel.__init__(self, root, *args, **kwargs)

        self.grid_rowconfigure(0, weight=0)  # title
        self.grid_rowconfigure(1, weight=1)  # avatars
        self.grid_rowconfigure(2, weight=0)  # buttons

        title = tk.Label(self, text="Select Avatar", font=("Helvetica", 12))
        title.grid(row=0, column=0, pady=15, padx=15)

        self.avatars_frame = tk.Frame(self)
        self.avatars_frame.grid(row=1, column=0)
        self.loaded_images = []
        self._selected_image_path = tk.StringVar()

        default_dir = join(getcwd(), "quince/ui/assets/avatars")
        avatars = get_files_from_dir(default_dir)

        self.callback = callback
        self.selected_avatar_path = "path"
        self.place_images(avatars)

        btn = tk.Button(self, text="OK", command=self.submit)
        btn.grid(row=2, column=0, pady=15, padx=4)

    def submit(self):
        """Closes window and sends path to avatar to the callback function."""
        self.callback(self._selected_image_path.get())
        self.destroy()

    def place_images(self, paths):
        """Creates a series of radio buttons with the images provided.

        Args:
            paths (list of string) - Absolute paths to images to be used.

        """
        self.loaded_images = []

        grid_position = GridPosition(5)
        for path in paths:
            try:
                img = Image.open(path)
                img.thumbnail((65, 65), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(img)
            except Exception:
                continue

            btn = tk.Radiobutton(
                self.avatars_frame,
                image=image,
                variable=self._selected_image_path,
                value=path,
                indicatoron=0,
                borderwidth=0,
                relief="flat",
                selectcolor="burlywood1",
                )
            btn.image = image

            self.loaded_images.append(btn)

            row, col = grid_position.get_value()
            btn.grid(row=row, column=col, padx=4, pady=4)
            grid_position.increment_right()
