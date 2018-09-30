"""
Class containing the "About" window
and a factory that can be injected into
the main tkinter app.
"""
import tkinter as tk
import webbrowser

LARGE_FONT = ("Helvetica", 18)


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

        appname = tk.Label(window,
                           text="Quince",
                           font=LARGE_FONT,
                           )
        appname.pack(pady=pady, padx=padx)

        version = tk.Label(window, text="Version:\t1.0 Release 1")
        version.pack(pady=pady, padx=padx)

        released = tk.Label(window, text="Released:\tPending")
        released.pack(pady=pady, padx=padx)

        link = tk.Label(window,
                        text="www.danliberatori.com",
                        fg="blue",
                        cursor="hand2",
                        )
        link.pack(pady=pady, padx=padx)
        link.bind('<Button-1>', open_link)

        ok_btn = tk.Button(window, text="Close", command=window.destroy)
        ok_btn.pack(pady=15, padx=padx)

        return window


def open_link(x):
    webbrowser.open_new(r"http://www.danliberatori.com")
