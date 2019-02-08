# App description

import tkinter as tk
import settings           # Application settings and constant variables.
import helpers            # Supporting classes for main application.
from PIL import Image

class HandSim(tk.Frame):


    def __init__(self, master):
        super().__init__(master)
        self.master = master

        helpers.deck_populate()

        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title(settings.TITLE)
        self.config(bg=settings.BACKGROUND)

    def create_widgets(self):
        player_1 = helpers.Player(self, 'Player 1')
        player_1.pack(pady=(20,20))



if __name__ == "__main__":
    root = tk.Tk()
    HandSim(root).pack(side='top', fill='both', expand=True)
    root.mainloop()