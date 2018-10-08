"""
Root tkinter window.
"""
import tkinter as tk


class GameApp(tk.Tk):
    """Root tkinter window hosting the entire app.
    """
    def __init__(self, AboutFactory, HowToPlay, TopMenuFactory, ScoreReport):
        tk.Tk.__init__(self)
        self.winfo_toplevel().title("Quince")
        self.minsize(800, 600)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.how_to_play = HowToPlay
        self.about_factory = AboutFactory
        self.frames["TopMenu"] = TopMenuFactory.generate(self.container,
                                                         self._start_new_game)
        self.frames["TopMenu"].grid(row=0, column=0, sticky="nsew")

        self.frames["scores"] = ScoreReport.generate(self.container,
                                                     self.start_next_round,
                                                     self.return_to_top)
        self.frames["scores"].grid(row=0, column=0, sticky="nsew")

        self._build_menus()
        self.show_frame("TopMenu")

    def return_to_top(self):
        self.show_frame("TopMenu")

    def _start_new_game(self, game_frame_factory):
        dummy = tk.Frame(self)
        previous_game = self.frames.get("GameFrame", dummy)

        previous_game.destroy()

        frame = game_frame_factory.generate(self.container,
                                            self.display_scores)
        self.frames["GameFrame"] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("GameFrame")

    def start_next_round(self):
        """Brings up the current game frame, initializing a new round."""
        frame = self.frames.get("GameFrame", None)

        if frame is None:
            print("Error! Attempting to start new round "
                  "with nonexistent game.")
            return

        frame.start_new_ronda()
        self.show_frame("GameFrame")
        frame.draw()
        frame.play_next_move()

    def show_frame(self, key):
        """Raises a frame to the top of the view.

        Args:
            key (string) - Dictionary key for the frame to raise
        """
        self.frames[key].tkraise()

    def _build_menus(self):
        """Generates the file menu, etc.
        """
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Game",
                             command=lambda: self.show_frame("TopMenu"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Game", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="How To Play", command=self._show_howtoplay)
        helpmenu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # probably unnecessary, but here for legacy compatibility
        self.option_add("*tearOff", tk.FALSE)
        self.config(menu=menubar)

    def _show_about(self):
        self.about_factory.generate(self)

    def _show_howtoplay(self):
        self.how_to_play.generate(self)

    def display_scores(self, ronda, updated_scores):
        """Updates and brings up the scores panel.
        """
        self.frames["scores"].update_scores(ronda, updated_scores)
        self.show_frame("scores")
