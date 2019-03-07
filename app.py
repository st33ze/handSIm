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
        # Creates header.
        text = 'Texas Holdem Hands Simulator'
        tk.Label(self, bg=settings.BACKGROUND, text=text, fg=settings.FOREGROUND,
                 font=settings.HEADER_FONT).grid(row=0)
        

        self.main_window = helpers.MainWindow(self)
        self.main_window.grid(row=1, pady=(10,40))
    
    def reset_app(self):
        '''Resets application to pre simulation view.'''
        self.main_window.grid_forget()
        self.main_window = helpers.MainWindow(self)
        self.main_window.grid(row=1, pady=(10,40))
        


if __name__ == "__main__":
    root = tk.Tk()
    HandSim(root).pack(side='top', fill='both', expand=True)
    root.mainloop()