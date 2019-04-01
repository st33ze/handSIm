# App description

import tkinter as tk
import settings as stg  # Application settings and constant variables.
import helpers          # Supporting classes for main application.

class HandSim(tk.Frame):


    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Set mouse focus for all widgets.
        self.master.bind_all('<1>', lambda event: event.widget.focus_set())

        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title(stg.TITLE)
        self.config(bg=stg.BACKGROUND)
        self.parent.geometry('765x600')

    def create_widgets(self):
        # Header.
        tk.Label(self, bg=stg.BACKGROUND, text=stg.HEADER , fg=stg.FOREGROUND,
                 font=stg.HEADER_FONT).grid(row=0)

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