"""
Tkinter frame shown when a ronda finishes.
Displays the scores earned during the round.
"""
import tkinter as tk
from quince.ui.components.score_report.card_scroll import CardScroll


class ScoreReport(tk.Frame):
    """Tk frame that shows scores after a ronda"""
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=0)
        self.grid_rowconfigure(7, weight=0)
        self.grid_rowconfigure(8, weight=0)
        self.grid_rowconfigure(9, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title = tk.Label(self, text="Scores")
        self.title.grid(row=0, column=0)

        self.siete_label = tk.Label(self, text="Siete de Velo:")
        self.siete_label.grid(row=1, column=0)
        self.siete = tk.Label(self, text="")
        self.siete.grid(row=1, column=1)

        self.most_cards_label = tk.Label(self, text="Most Cards:")
        self.most_cards_label.grid(row=2, column=0)
        self.most_cards = tk.Label(self, text="")
        self.most_cards.grid(row=2, column=1)

        self.most_oros_label = tk.Label(self, text="Most Golds:")
        self.most_oros_label.grid(row=3, column=0)
        self.most_oros = tk.Label(self, text="")
        self.most_oros.grid(row=3, column=1)

        self.setenta_label = tk.Label(self, text="Setenta:")
        self.setenta_label.grid(row=4, column=0)
        self.setenta = tk.Label(self, text="")
        self.setenta.grid(row=4, column=1)

        self.escobas_label = tk.Label(self, text="Escobas:")
        self.escobas_label.grid(row=5, column=0)
        self.escobas = tk.Label(self, text="")
        self.escobas.grid(row=5, column=1)

    def update_scores(self, ronda):
        scores = ronda.calculate_scores()

        siete = scores.get('7_de_velo', "Score Error")
        self.siete.config(text=siete)

        most_cards = scores.get('most_cards', "Score Error")
        self.most_cards.config(text=most_cards)

        most_oros = scores.get('most_oros', "Score Error")
        self.most_oros.config(text=most_oros)

        setenta = scores.get('setenta', "Score Error")
        self.setenta.config(text=setenta)

        escobas = scores.get('escobas', 'Score Error')
        self.escobas.config(text=escobas)

        # This will blow up when we try to update scores after
        # more than one ronda
        row = 6
        for player in ronda.player_cards:
            pila = ronda.player_cards[player]['pila']
            C = pila.get_cards()
            cards = C['oro'] + C['copa'] + C['espada'] + C['basto']
            scroll = CardScroll(self, player.image(), cards)
            scroll.grid(row=row,
                        column=0,
                        columnspan=2,
                        sticky="sew",
                        pady=10,
                        padx=(35, 10))
            row += 1

    @staticmethod
    def generate(root):
        """Generates a score report frame.

        Args:
            root (tk widget) - parent widget for the scorereport frame

        Returns:
            ScoreReport (tkFrame)
        """
        return ScoreReport(root)
