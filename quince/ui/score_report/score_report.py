"""
Tkinter frame shown when a ronda finishes.
Displays the scores earned during the round.
"""
import tkinter as tk
from os.path import join
from os import getcwd
from PIL import Image, ImageTk
from quince.ui.score_report.card_scroll import CardScroll


IMG_ROOT = join(getcwd(), "quince/assets/scores")


def load_image(file_name):
    """Returns a png image as a PhotoImage object"""
    path = join(IMG_ROOT, file_name)
    img = Image.open(path)
    return ImageTk.PhotoImage(img)


class ScoreSummary(tk.Frame):
    """Shows who earned points in each category"""
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        for r in range(0, 10):
            self.grid_columnconfigure(r, weight=1)

        padx = (24, 4)

        img = load_image("cards.png")
        cards = tk.Label(self, image=img)
        cards.img = img
        cards.grid(row=0, column=0, padx=padx, sticky="nsew")
        self.cards = tk.Label(self, text="Winners")
        self.cards.grid(row=0, column=1, sticky="nsew")

        img = load_image("oros.png")
        oros = tk.Label(self, image=img)
        oros.img = img
        oros.grid(row=0, column=2, padx=padx, sticky="nsew")
        self.oros = tk.Label(self, text="Oros winners")
        self.oros.grid(row=0, column=3, sticky="nsew")

        img = load_image("siete.png")
        siete = tk.Label(self, image=img)
        siete.img = img
        siete.grid(row=0, column=4, padx=padx, sticky="nsew")
        self.siete = tk.Label(self, text="7 winner")
        self.siete.grid(row=0, column=5, sticky="nsew")

        img = load_image("setenta.png")
        setenta = tk.Label(self, image=img)
        setenta.img = img
        setenta.grid(row=0, column=6, padx=padx, sticky="nsew")
        self.setenta = tk.Label(self, text="7a winners")
        self.setenta.grid(row=0, column=7, sticky="nsew")

        img = load_image("escobas.png")
        escobas = tk.Label(self, image=img)
        escobas.img = img
        escobas.grid(row=0, column=8, padx=padx, sticky="nsew")
        self.escobas = tk.Label(self, text="escobas winners")
        self.escobas.grid(row=0, column=9, sticky="nsew")

    def set_winners(self, cards, oros, siete, setenta, escobas):
        """Updates the text on the labels for each of the
        score categories.

        Args:
            cards, oros, siete, setenta escobas
            -- Strings to display on their respoective labels
        """
        self.cards.config(text=cards)
        self.oros.config(text=oros)
        self.siete.config(text=siete)
        self.setenta.config(text=setenta)
        self.escobas.config(text=escobas)


class ScoreReport(tk.Frame):
    """Tk frame that shows scores after a ronda"""
    def __init__(self, root, callback):
        """Instantiates a ScoreReport frame.

        Args:
            root (tk widget) - parent container
            callback (function) - Function to execute
            when clicking the "Next Round" button.
        """
        tk.Frame.__init__(self, root)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title = tk.Label(self,
                              text="This round's scores",
                              font=("Helvetica", 14))
        self.back_btn = tk.Button(self,
                                  text="Next Round",
                                  command=callback)
        self.title.grid(row=0, column=0)
        self.back_btn.grid(row=0, column=0, sticky="e", padx=10)

        self.summary = ScoreSummary(self)
        self.summary.grid(row=1, column=0)

        self.scrolls = []

    def update_scores(self, ronda, updated_scores):
        scores = ronda.calculate_scores()

        siete_winner = scores.get("7_de_velo", None)
        siete = siete_winner.name  # should probably check for None here?

        (cards_winners, count) = scores.get("most_cards", ([], 0))
        cards = str(count)
        for player in cards_winners:
            cards += f"\n{player.name}"

        (oros_winners, count) = scores.get("most_oros", ([], 0))
        oros = str(count)
        for player in oros_winners:
            oros += f"\n{player.name}"

        setenta_winners = scores.get("setenta", [])
        winners = [w.player.name for w in setenta_winners]
        setenta = "\n".join(winners)

        escobas_winners = scores.get("escobas", [])
        winners = [f"{w[0].name}: {w[1]}" for w in escobas_winners]
        escobas = "\n".join(winners)

        self.summary.set_winners(cards, oros, siete, setenta, escobas)

        for scroll in self.scrolls:
            scroll.destroy()

        row = 3
        for player in ronda.player_cards:
            pila = ronda.player_cards[player]["pila"]
            C = pila.get_cards()
            cards = C["oro"] + C["copa"] + C["espada"] + C["basto"]
            scroll = CardScroll(self, player.image(), cards)
            scroll.grid(row=row,
                        column=0,
                        sticky="sew",
                        pady=10,
                        padx=(35, 10))
            self.scrolls.append(scroll)
            row += 1

    @staticmethod
    def generate(root, callback):
        """Generates a score report frame.

        Args:
            root (tk widget) - parent widget for the scorereport frame
            callback (function) - Callback to execute when clicking
            the "play next round" button.

        Returns:
            ScoreReport (tkFrame)
        """
        return ScoreReport(root, callback)
