# HandSim is a Texas Holdem game simulator. It gets cards chosen by player, or picks
# random cards by itself as input. Then it simulates number of games and shows results.
# Simulation is done in a seperate thread, to make GUI responsive. If simulation
# takes longer than few seconds progress bar appears to inform user how much time it is
# going to take. Application also saves and averages simulation times. The more games it
# simulates, the more accurate time estimations are.  

import tkinter as tk
import settings as stg  # Application settings and constant variables.
import helpers          # Supporting classes for main application.

class HandSim(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        helpers.load_graphics()
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title(stg.TITLE)
        self.config(bg=stg.BACKGROUND)
        self.parent.geometry(stg.APP_SIZES['default'][0])

    def create_widgets(self):
        # Header.
        tk.Label(self, bg=stg.BACKGROUND, text=stg.HEADER , fg=stg.FOREGROUND,
                 font=stg.HEADER_FONT).grid(row=0)

        self.menubar = helpers.MenuBar(self)
        self.parent.config(menu=self.menubar)

        self.main_window = helpers.MainWindow(self)
        self.main_window.grid(row=1, pady=(10,40))
    
    def reset_view(self):
        '''Resets application view to pre simulation.'''
        self.main_window.destroy()
        self.main_window = helpers.MainWindow(self)
        self.main_window.grid(row=1, pady=(10,40))


if __name__ == "__main__":
    root = tk.Tk()
    HandSim(root).pack(side='top', fill='both', expand=True)
    root.mainloop()