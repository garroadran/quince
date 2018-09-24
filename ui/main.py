import tkinter as tk
import os
from PIL import Image, ImageTk
from ui.components.opponents.opponent_frame import OpponentFrameHorizontal, OpponentFrameVertical

LARGE_FONT = ("Verdana", 12)


class GameApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._build_menus()

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)
        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

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


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label = tk.Label(self, text="Hello!", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)

        relpath = f'ui/assets/avatars/alice.png'
        image_path = os.path.join(os.getcwd(), relpath)
        avatar_img = Image.open(image_path)
        player_name = "Alice"
        is_active = True
        hand_size = 3

        # opp1 = OpponentFrameHorizontal(self, avatar_img, player_name, is_active, hand_size)
        # opp1.pack()

        opp2 = OpponentFrameVertical(self, avatar_img, player_name, is_active, hand_size)
        opp2.pack()

app = GameApp()
app.mainloop()
