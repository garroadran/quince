"""
Class containing the "About" window
and a factory that can be injected into
the main tkinter app.
"""
from os import getcwd, path
import tkinter as tk
import webbrowser
from PIL import Image, ImageTk
from quince.version import __version__


LARGE_FONT = ("Helvetica", 20)


class AboutFactory(object):
    """Builds an About window"""
    def generate(self, root):
        """
        Args:
            root (tk widget)

        Returns:
            Tk Frame widget
        """
        padx = 30
        pady = 10

        window = tk.Toplevel(root)

        window.winfo_toplevel().title("About")
        window.resizable(width=False, height=False)

        icon = Image.open(path.join(getcwd(), "quince/assets/favicon_32.png"))
        img = ImageTk.PhotoImage(icon)
        appname = tk.Label(window,
                           text="Quince",
                           font=LARGE_FONT,
                           image=img,
                           compound="left"
                           )
        appname.img = img
        appname.pack(pady=pady, padx=padx)

        version = tk.Label(window, text=f"Version:\t{__version__}")
        version.pack(pady=pady, padx=padx)

        link = tk.Label(window,
                        text="www.danliberatori.com",
                        fg="blue",
                        cursor="hand2",
                        )
        link.pack(pady=pady, padx=padx)
        link.bind("<Button-1>", open_link)

        ok_btn = tk.Button(window, text="Close", command=window.destroy)
        ok_btn.pack(pady=15, padx=padx)

        return window


def open_link(x):
    webbrowser.open_new(r"http://www.danliberatori.com")
