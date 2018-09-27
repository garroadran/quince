"""
Root tkinter window.
"""
import tkinter as tk

class GameApp(tk.Tk):
    """Root tkinter window hosting the entire app.
    """
    def __init__(self, GameFrameFactory, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("Quince")
        self.minsize(800, 600)

        self._build_menus()

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = GameFrameFactory.generate(container)
        self.frames['GameFrame'] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('GameFrame')

    def show_frame(self, controller):
        """
            Raises a frame to the top of the view.

        Args:
            controller - tk frame to raise to the top of the view
        """
        frame = self.frames[controller]
        frame.tkraise()

    def _build_menus(self):
        """
            Generates the file menu, etc.
        """
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.quit)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)
