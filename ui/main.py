import tkinter as tk
import os
from PIL import Image, ImageTk
from ui.components.opponents.opponent_frame import OpponentFrameHorizontal, OpponentFrameVertical
from ui.components.player.player_frame import PlayerFrame

LARGE_FONT = ("Verdana", 12)


class GameApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("Quince")
        self.minsize(600, 600)

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

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        # OPPONENT 1
        opp1_path = os.path.join(os.getcwd(), 'ui/assets/avatars/alice.png')
        opp1_img = Image.open(opp1_path)
        opp1_name = "Alice"
        opp1_active = False
        opp1_hand_size = 3
        opp1 = OpponentFrameVertical(self, opp1_img, opp1_name, opp1_active, opp1_hand_size)
        opp1.grid(row=1, column=0)

        # OPPONENT 2
        opp2_path = os.path.join(os.getcwd(), 'ui/assets/avatars/bob.png')
        opp2_img = Image.open(opp2_path)
        opp2_name = "Bob"
        opp2_active = False
        opp2_hand_size = 3
        opp2 = OpponentFrameHorizontal(self, opp2_img, opp2_name, opp2_active, opp2_hand_size)
        opp2.grid(row=0, column=1)
        
        # OPPONENT 3
        opp3_path = os.path.join(os.getcwd(), 'ui/assets/avatars/charlie.png')
        opp3_img = Image.open(opp3_path)
        opp3_name = "Charlie"
        opp3_active = False
        opp3_hand_size = 3
        opp3 = OpponentFrameVertical(self, opp3_img, opp3_name, opp3_active, opp3_hand_size)
        opp3.grid(row=1, column=2)

        # PLAYER
        hud = PlayerFrame(self)
        hud.grid(row=2, column=0, columnspan=3)




app = GameApp()
app.mainloop()
