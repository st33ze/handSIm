# Classes and functions supporting main application.

import glob, os
import tkinter as tk
from PIL import Image, ImageTk
import settings  # Application settings and constant variables.




class Player(tk.LabelFrame):

    ''' 
        Player frame, with main window as a parent, containing two Card classes.
        Displays two-card hand set.
    '''

    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        
        self.config_frame()
        self.create_widgets()


    def config_frame(self):
        # self.config(width = 100, height = 100)
        self['bg'] = settings.BACKGROUND
        self['fg'] = settings.FOREGROUND
        self['text'] = self.name


    def create_widgets(self):
        card_1 = Card(self)
        card_1.pack(pady=(10,10))



class Card(tk.Frame):

    '''
        Card frame, with Player class as a parent. Displays a card, with buttons
        to change card type and color. 
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.rbutton_option = tk.IntVar()
        self.rbutton_option.set(4) # Initialize first as backside card.
        self.current_card = [None, None] # [Card color, card symbol]

        self.config_frame()
        self.create_widgets()
        

    def config_frame(self):
        self['bg'] = settings.BACKGROUND
        # self['fg'] = settings.FOREGROUND


    def create_widgets(self):
        # Create card image.
        self.show_card(self.current_card)
        
        # Create card colors radiobuttons.
        self.create_radiobutton('clubs', 0)
        self.create_radiobutton('diamonds', 1)
        self.create_radiobutton('hearts', 2)
        self.create_radiobutton('spades', 3)

        # Create next and prev buttons.
        self.create_button('prev', 0, False)
        self.create_button('next', 2, True)
    

    def show_card(self, card):
        # Initialize card as backside view.
        option = self.rbutton_option.get()
        if option == 4:
            img = ImageTk.PhotoImage(Image.open(settings.IMG_DIR + 'backside.png'))
        
        # Show current card.
        else:
            # Set file name to open.
            color = card[0]
            symbol = card[1]
            if symbol < 10:
                file_name = settings.IMG_DIR + str(color) + '0' + str(symbol) + '.png'
            else:
                file_name = settings.IMG_DIR + str(color) + str(symbol) +  '.png'
            img = ImageTk.PhotoImage(Image.open(file_name))
            
            # Update deck
            settings.CARD_DECK[color][symbol] = None

        card = tk.Label(self, image=img, bg=settings.BACKGROUND)
        card.image = img
        card.grid(row=0, columnspan=4, pady=(0,10))

        
    def create_radiobutton(self, img_name, val):
        '''Creates radiobutton with image as label. '''
        img = ImageTk.PhotoImage(Image.open(settings.IMG_DIR + img_name + '.png'))
        button = tk.Radiobutton(self, image=img, bg=settings.BACKGROUND, bd=0,
                                activebackground=settings.BACKGROUND, 
                                highlightthickness=0, variable=self.rbutton_option,
                                value=val, command=lambda: self.switch_color(val))
        button.image = img
        button.grid(row=1, column=val)
        return button


    def create_button(self, img_name, val, switcher):
        ''' Creates button as image.'''
        img = ImageTk.PhotoImage(Image.open(settings.IMG_DIR + img_name + '.png'))
        button = tk.Button(self, image=img, bg=settings.BACKGROUND, bd=0,
                           activebackground=settings.BACKGROUND, highlightthickness=0,
                           command=lambda: self.switch_card(self.current_card[0], 
                           self.current_card[1], switcher))
        button.image = img
        button.grid(row=2, column=val, columnspan=2, pady=(10,0))


    def switch_color(self, color):
        '''Changes color of the current card.'''
        symbol = -1 # Reset symbol.
        self.switch_card(color, symbol, True)
        
    
    def switch_card(self, color, symbol, switcher):
        '''Changes to the nearest avalaible card.'''
        if color is not None and symbol is not None:
            self.update_deck(self.current_card)
            # Look in positive direction.
            if switcher:
                symbol += 1
                while(symbol > 12 or settings.CARD_DECK[color][symbol] == None):
                    # If outside card range, reset.
                    if symbol > 12:
                        symbol = 0
                    else:
                        symbol += 1
            # Look in negative drieciton.
            else:
                symbol -= 1
                while(symbol < 0 or settings.CARD_DECK[color][symbol] == None):
                    # If outside card range, reset backwards.
                    if symbol < 0:
                        symbol = 12
                    else:
                        symbol -= 1
            
            # Update current_card variable and show new card.
            self.current_card[0] = color
            self.current_card[1] = symbol
            self.show_card(self.current_card)
            settings.CARD_DECK[color][symbol] = None


    def update_deck(self, card):
        '''Deletes None value from CARD_DECK if card is not used anymore.'''
        if card[0] is not None and card[1] is not None:
            settings.CARD_DECK[card[0]][card[1]] = card[1]



def card_resize(scale, path, save_path):
    '''Script helping to resize original card images.'''
    # Change size for every png image in the path folder.    
    for image in glob.glob(path + '.png'):
        img = Image.open(image)
        # Set new size of the image.
        changed_size = (int(img.size[0] * scale), int(img.size[1] * scale))
        # Get name from the file path.
        name = os.path.split(image)[1]
        # Resize and save the image
        img = img.resize(changed_size, Image.ANTIALIAS)
        os.makedirs(os.path.dirname(save_path + name), exist_ok=True)
        img.save(save_path + name, quality=90)
        img.close()


def deck_populate():
    '''Populates CARD_DECK variable.'''
    for _ in range(4):
        settings.CARD_DECK.append(list(range(13))) 
