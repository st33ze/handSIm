# App description

import tkinter as tk
import settings           # Application settings and constant variables.
import helpers            # Supporting classes for main application.
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
        background = settings.BACKGROUND
        foreground = settings.FOREGROUND
        # Creaters header.
        text = 'Texas Holdem Hands Simulator'
        tk.Label(self, bg=background, text=text, fg=foreground,
                 font=settings.HEADER_FONT).grid(row=0, columnspan=2)
        
        # Creates players frames.
        player_1 = helpers.Player(self, 'Player 1')
        player_1.grid(row=1, column=0, pady=(10,20), padx=(10,30))
        player_2 = helpers.Player(self, 'Player 2')
        player_2.grid(row=1, column=1, pady=(10,20), padx=(30,10))

        # Simulation amount input frame.
        user_input = helpers.Sim_quantity(self)
        user_input.grid(row=2, column=0, pady=(50,50))

        # Simulation button
        tk.Button(self, text='Simulate', bg=settings.COLOR, relief='flat',
                  highlightbackground=background, highlightcolor=background, 
                  fg=foreground, activebackground=foreground, font=settings.FONT,
                  activeforeground=background, highlightthickness=2,
                  command=lambda: self.simulate(user_input.value.get())).grid(row=2, 
                  column=1, pady=(50,50))
    
    def simulate(self, sim_amount):
        print(sim_amount)
        






if __name__ == "__main__":
    root = tk.Tk()
    HandSim(root).pack(side='top', fill='both', expand=True)
    root.mainloop()