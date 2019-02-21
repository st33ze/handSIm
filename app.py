# App description

import tkinter as tk
import settings           # Application settings and constant variables.
import helpers          # Supporting classes for main application.
from PIL import Image

class HandSim(tk.Frame):


    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # Set mouse focus for all widgets.
        self.master.bind_all('<1>', lambda event: event.widget.focus_set())
        helpers.deck_populate()

        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title(settings.TITLE)
        self.config(bg=settings.BACKGROUND)

    def create_widgets(self):
        # players = []
        # Creates header.
        text = 'Texas Holdem Hands Simulator'
        tk.Label(self, bg=settings.BACKGROUND, text=text, fg=settings.FOREGROUND,
                 font=settings.HEADER_FONT).grid(row=0)
        
        # # Creates players frames.
        # player_1 = helpers.Player(self, 'Player 1')
        # player_1.grid(row=1, column=0, pady=(10,20), padx=(10,30))
        # player_2 = helpers.Player(self, 'Player 2')
        # player_2.grid(row=1, column=1, pady=(10,20), padx=(30,10))

        # players.append(player_1)
        # players.append(player_2)

        # # Simulation amount input frame.
        # user_input = helpers.SimQuantity(self)
        # user_input.grid(row=3, column=0, pady=(25,50))

        # # # Simulation button
        # sim_button = helpers.Simulate(self, players, user_input)
        # sim_button.grid(row=3, column=1, pady=(25,50))

        preSim = helpers.PreSim(self)
        preSim.grid(row=1, pady=(10,40))
        


if __name__ == "__main__":
    root = tk.Tk()
    HandSim(root).pack(side='top', fill='both', expand=True)
    root.mainloop()