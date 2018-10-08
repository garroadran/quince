"""Generates a window that shows
the basics of how the game is played."""

import tkinter as tk


FRAME_WIDTH = 500


class HowToPlay(tk.Toplevel):
    """Window element that teaches players how to play the game."""
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.winfo_toplevel().title("How To Play")
        self.resizable(False, False)

        self.canvas = tk.Canvas(self,
                                width=FRAME_WIDTH,
                                height=450)
        # self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.bar = tk.Scrollbar(self,
                                orient="vertical",
                                command=self.canvas.yview)
        # self.bar.grid(row=0, column=1, sticky="ns")
        self.bar.pack(side="right", fill="y", expand=True)

        self.text_frame = tk.Frame(self.canvas)
        self.canvas_item = self.canvas.create_window((0, 0),
                                                     window=self.text_frame,
                                                     anchor="nw")
        self.canvas.config(yscrollcommand=self.bar.set)

        self.canvas.bind("<Configure>", self._framewidth)
        self.text_frame.bind("<Configure>", self._onframeconfigure)

        self._pack_title("How To Play")

        self._pack_subheader("Initial deal")
        self._pack_para("Each player gets dealt 3 cards, and then 4 cards "
                        "are dealt face up on the table.")
        self._pack_para("If by chance the 4 cards on the table add up "
                        "to 15, then the player who dealt automatically "
                        "picks up the cards and scores an Escoba.")

        self._pack_subheader("Special card values")
        self._pack_para("Escoba De Quince, is played with card values from "
                        "1 to 10, however, the game is traditionally played "
                        "with a deck of cards that does not contain the "
                        "numbers 8 or 9.")
        self._pack_para("As a result, the three face cards "
                        "(known as the Page, the Horse, and the King, with "
                        "the numbers 10, 11, and 12 respectively) have "
                        "real values of 8, 9, and 10, respectively.")
        self._pack_para("This means that in order to pick up a King, "
                        "players will need to combine it with a 5 (since "
                        "10 + 5 = 15), in order to pick up a Horse, "
                        "players will need to combine it with a 6 (since "
                        "9 + 6 = 15), and in order to pick up a Page "
                        "players will need to combine it with a 7 (since "
                        "8 + 7 = 15). This can be somewhat confusing at "
                        "first, but it is fairly easy to get accustomed to.")

        self._pack_subheader("Pick up cards")
        self._pack_para("Starting to the left of the dealer, players "
                        "take turns. On their turn, a player must either use "
                        "one of the cards in their hand to pick up cards "
                        "from the table, or lay down one of their cards "
                        "on the table.")
        self._pack_para("In order to pick up cards, the value of card from "
                        "the player's hand must be added together with the "
                        "values of the cards they collect from the table. "
                        "If together they add up to 15, then they can be "
                        "picked up.")
        self._pack_para("Example pickups:")
        self._pack_para("From hand: 7.\tFrom table: 8")
        self._pack_para("From hand: 5.\tFrom table: 4, 6")
        self._pack_para("From hand: 2.\tFrom table: 1, 1, 4, 4, 3")
        self._pack_para("If the player does not have any legal pickups "
                        "available, they have no choice but to simply "
                        "lay down one of their cards on the table, which "
                        "other players can then proceed to pick up.")
        self._pack_para("When a player picks up cards from the table, they "
                        "do not put these cards back into their hand. "
                        "Instead, they put their picked-up cards on a "
                        "separate pile of cards which they keep face-down "
                        "on the table.")

        self._pack_subheader("Escobas")
        self._pack_para("If, during their turn, a player manages to pick up "
                        "all of the cards on the table (thus leaving an "
                        "empty table for the next player, who will have "
                        "no choice but to drop one of their own cards), "
                        "this is called an \"Escoba\".")
        self._pack_para("Each escoba that a player makes is worth 1 point.")

        self._pack_subheader("Finishing a round")
        self._pack_para("Once each player has played three times (and "
                        "thus used up all of the cards in their hand, the "
                        "round is completed. Any cards that remain on the "
                        "on the table are automatically awarded to the last "
                        "player who picked up cards. Scores for the round "
                        "are counted and added to the totals for the game.")
        self._pack_para("The cards are collected, shuffled, and dealt again. "
                        "Players take turns dealing the cards each round.")
        self._pack_para("The game ends when one or more players have "
                        "accumulated 30 points.")

        self._pack_subheader("Scoring")
        self._pack_para("At the end of each round, players can earn points "
                        "for completing different achievements. In the case "
                        "of ties (eg. If two players each picked up 12 cards) "
                        "all tied players are awarded the points.")
        self._pack_para("Picked up the most cards: 1 point")
        self._pack_para("Picked up the most golds (oros): 1 point")
        self._pack_para("Picked up the 7 of gold (the \"Siete de velo\"):"
                        "1 point")
        self._pack_para("Best \"Setenta\": 1 point")

        self._pack_subheader("Setenta")
        self._pack_para("The \"Setenta\" is built by combining one card from "
                        "each suit. If a player has not picked up at least "
                        "one card from each suit they cannot build a setenta "
                        "and therefore have a setenta score of 0.")
        self._pack_para("The best possible setenta is comprised of four 7s "
                        "and is deemed to be worth 70 points (each 7 has a "
                        "setenta value of 17.5 points.")
        self._pack_para("The full scoring table is as follows:")
        self._pack_para("Ace (1): Worth 11 setenta points")
        self._pack_para("Two (2): Worth 4 setenta points")
        self._pack_para("Three (3): Worth 6 setenta points")
        self._pack_para("Four (4): Worth 8 setenta points")
        self._pack_para("Five (5): Worth 10 setenta points")
        self._pack_para("Six (6): Worth 14 setenta points")
        self._pack_para("Seven (7): Worth 17.5 setenta points")
        self._pack_para("Page (8): Worth 1 setenta point")
        self._pack_para("Horse (9): Worth 1 setenta point")
        self._pack_para("King (10): Worth 1 setenta point")

    def _pack_title(self, text):
        font = ("Helvetica", 16, "bold")

        lbl = tk.Label(self.text_frame, text=text, font=font, anchor="center")
        lbl.pack(pady=(20, 16))

    def _pack_subheader(self, text):
        font = ("Helvetica", 12, "bold")

        lbl = tk.Label(self.text_frame, text=text, font=font, anchor="w")
        lbl.pack(pady=(12, 8), padx=10, anchor="w")

    def _pack_para(self, text):
        font = ("Helvetica", 10)

        lbl = tk.Label(self.text_frame,
                       text=text,
                       font=font,
                       anchor="w",
                       justify="left",
                       wraplength=FRAME_WIDTH-20-10)
        lbl.pack(anchor="w", padx=(20, 10))

    def _framewidth(self, event):
        self.canvas.itemconfig(self.canvas_item, width=event.width)

    def _onframeconfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    @staticmethod
    def generate(root):
        return HowToPlay(root)
