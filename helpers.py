# Classes and functions supporting main application.

import random
import glob, os
import tkinter as tk
from PIL import Image, ImageTk
from collections import Counter
import settings  # Application settings and constant variables.
import tests

# TODO:
# * Check if parent variable is needed in those classes.
# * Remove original size images from repo?
# * Check if not better to set CARD_DECK as dictionary.
# * SUCCESS_COLOR


class PreSim(tk.Frame):
    '''Container with widgets of pre simulation view.'''

    def __init__(self, parent, players=2):
        super().__init__(parent)
        self.parent = parent
        self.player_amount = players

        self.config_frame()
        self.create_widgets()

    def config_frame(self):
        self['bg'] = settings.BACKGROUND
    
    def create_widgets(self):
        # Create players frames.
        players = []
        for _ in range(settings.PLAYER_MODE):
            players.append(Player(self, 'Player ' + str(_ + 1)))
        for player in players:
            if players.index(player) < len(players) - 1:
                player.grid(row=0, column=players.index(player), pady=(0,30),
                            padx=(10,40))
            else:
                player.grid(row=0, column=players.index(player), pady=(0,30),
                            padx=(10,10))
            
        # Simulation amount input  frame.
        user_input = SimQuantity(self)
        user_input.grid(row=2, column=0, pady=(10,0))

        # Simulation button.
        sim_button = Simulate(self, players, user_input)
        sim_button.grid(row=2, column=1, pady=(10,0))


class Player(tk.LabelFrame):
    ''' 
        Player frame, with main window as a parent, containing two Card classes.
        Displays two-card hand set.
    '''

    def __init__(self, parent, name):
        super().__init__(parent)
        self.parent = parent
        self.name = name
        self.cards = [] # Card objects.
        self.hand = [] # Player current hand.
        self.board = [] # Cards in current board.
        
        self.config_frame()
        self.create_widgets()


    def config_frame(self):
        self['bg'] = settings.BACKGROUND
        self['fg'] = settings.FOREGROUND
        self['text'] = self.name
        self['font'] = settings.FONT


    def create_widgets(self):
        card_1 = Card(self)
        card_1.grid(row=1, column=0, pady=(10,10), padx=(10,15))
        card_2 = Card(self)
        card_2.grid(row=1, column=1, pady=(10,10), padx=(15,10))

        self.cards.append(card_1)
        self.cards.append(card_2)
        self.hand.append(card_1.current_card)
        self.hand.append(card_2.current_card)
    
    def hand_update(self):
        self.hand = [self.cards[0].current_card, self.cards[1].current_card]
    
    def check_result(self):
        ''' Checks current result, depending on current hand and board cards.'''
        self.result = None
        cards = self.hand + self.board
        colors = []
        symbols = []

        for card in cards:
            # Get colors.
            colors.append(card[0])
            # Get symbols.
            symbols.append(card[1])
        symbols.sort()
        
        # Color check.
        colors = Counter(colors).most_common(1)
        if colors[0][1] >= 5:
            self.result = 'Color'
            # Poker check.




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
        self.changable_widgets = []

        self.config_frame()
        self.create_widgets()
        

    def config_frame(self):
        self['bg'] = settings.BACKGROUND
        # self['fg'] = settings.FOREGROUND


    def create_widgets(self):
        # Create card image.
        self.show_card(self.current_card)
        
        # Create card colors radiobuttons.
        clubs = self.create_radiobutton('clubs', 0)
        diamonds = self.create_radiobutton('diamonds', 1)
        hearts = self.create_radiobutton('hearts', 2)
        spades = self.create_radiobutton('spades', 3)

        # Create next and prev buttons.
        prev_btn = self.create_button('prev', 0, False)
        next_btn = self.create_button('next', 2, True)

        # Append widgets that will dynamically change.
        self.changable_widgets.append(clubs)
        self.changable_widgets.append(diamonds)
        self.changable_widgets.append(hearts)
        self.changable_widgets.append(spades)
        self.changable_widgets.append(prev_btn)
        self.changable_widgets.append(next_btn)

    def show_card(self, card):
        # Initialize card as backside view.
        if self.rbutton_option.get() == 4 and any(x is None for x in card):
            img = ImageTk.PhotoImage(Image.open(settings.IMG_DIR[0] + 'backside.png'))
        
        # Show current card.
        else:
            # Set file name to open.
            color = card[0]
            symbol = card[1]
            if symbol < 10:
                file_name = settings.IMG_DIR[0] + str(color) + '0' + str(symbol) + '.png'
            else:
                file_name = settings.IMG_DIR[0] + str(color) + str(symbol) +  '.png'
            img = ImageTk.PhotoImage(Image.open(file_name))
            
            # Update deck
            settings.CARD_DECK[color][symbol] = None

        card = tk.Label(self, image=img, bg=settings.BACKGROUND)
        card.image = img
        card.grid(row=0, columnspan=4, pady=(0,10))

        
    def create_radiobutton(self, img_name, val):
        '''Creates radiobutton with image as label. '''
        img = ImageTk.PhotoImage(Image.open(settings.IMG_DIR[0] + img_name + '.png'))
        button = tk.Radiobutton(self, image=img, bg=settings.BACKGROUND,
                                activebackground=settings.BACKGROUND, 
                                highlightthickness=0, variable=self.rbutton_option,
                                value=val, command=lambda: self.switch_color(val))
        button.image = img
        button.grid(row=1, column=val)
        return button


    def create_button(self, img_name, val, switcher):
        ''' Creates button as image.'''
        img = ImageTk.PhotoImage(Image.open(settings.IMG_DIR[0] + img_name + '.png'))
        button = tk.Button(self, image=img, bg=settings.BACKGROUND, bd=0,
                           activebackground=settings.BACKGROUND, highlightthickness=0,
                           command=lambda: self.switch_card(self.current_card[0], 
                           self.current_card[1], switcher))
        button.image = img
        button.grid(row=2, column=val, columnspan=2, pady=(10,0))
        return button


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



class SimQuantity(tk.Frame):
    '''Gets user simulation amount input.'''

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.changable_widgets = []
        self.value = tk.StringVar()
        self.value.set(100)

        self.config_frame()
        self.create_widgets()

    def config_frame(self):
        self['bg'] = settings.BACKGROUND

    def create_widgets(self):
        input_label = tk.Label(self, text='Simulations amount:', bg=settings.BACKGROUND, 
                               font=settings.FONT, fg=settings.FOREGROUND)
        input_entry = tk.Entry(self, textvariable=self.value, width=6, relief='flat',
                               bg=settings.BACKGROUND, fg=settings.FOREGROUND,
                               insertbackground=settings.SUCCESS_COLOR,
                               highlightbackground=settings.BACKGROUND,
                               highlightcolor=settings.BACKGROUND,
                               disabledbackground=settings.BACKGROUND,
                               font=settings.FONT)
        input_label.grid(row=0, column=0)
        input_entry.grid(row=0,column=1)
        
        self.changable_widgets.append(input_label)
        self.changable_widgets.append(input_entry)



class Simulate(tk.Button):
    ''' Simulation algorithm and user input validadion.'''
    
    def __init__(self, parent, players, input_obj):
        super().__init__(parent)
        self.parent = parent
        self.players_obj = players # Reference to players objects list.
        self.input_obj = input_obj # Reference to input object.
        self.show_error = None # Show error label.
        self.error = None # Error message.
        self.test_counter = 0 # For simulation tests.

        self.widget_config()

    def widget_config(self):
        self['text'] = 'Simulate'
        self['relief'] = 'flat'
        self['font'] = settings.FONT
        self['bg'] = settings.SUCCESS_COLOR
        self['fg'] = settings.FOREGROUND
        self['highlightbackground'] = settings.BACKGROUND
        self['highlightcolor'] = settings.BACKGROUND
        self['activebackground'] = settings.FOREGROUND
        self['activeforeground'] = settings.BACKGROUND
        self['highlightthickness'] = 2
        self['command'] = lambda: self.simulate()
    
    def simulate(self):
        if settings.TEST_MODE:
            self.sim_test()

        else:
            ''' Simulation algorithm.'''
            user_input = self.input_obj.value.get()
            
            # Delete old error label if exists.
            if self.show_error:
                self.show_error.grid_forget()
            
            # If input value is correct, simulate games.
            sim_amount = self.validate_input(user_input)
            if sim_amount:
                
                # Set all the button and input widgets as disabled.
                for player in self.players_obj:
                    for card in player.cards:
                        for widget in card.changable_widgets:
                            widget['state'] = 'disabled'
                for widget in self.input_obj.changable_widgets:
                    widget['state'] = 'disabled'
                self['state'] = 'disabled'

                # Check for blank cards.
                cards_to_random = []
                deck = list(range(1, 53))
                for player_object in self.players_obj:
                    for card in player_object.cards:
                        if any(x is not None for x in card.current_card):
                            deck.remove(card.current_card[0] * 13 + 
                                        (card.current_card[1] + 1))
                        else:
                            cards_to_random.append(card)
                # If blank pick random cards.
                for card in cards_to_random:
                    random_card = random.choice(deck)
                    card.current_card = [(random_card - 1) // 13, (random_card -1) % 13]
                    card.show_card(card.current_card)
                    deck.remove(random_card)
                
                # Update players hands.
                for player in self.players_obj:
                    player.hand_update()
                
                
                # Simulate sim_amount games.
                self.sim_game(deck)
                    
            # Else raise an error.
            else:
                self.show_error = tk.Label(self.parent, text=self.error, 
                                           bg=settings.BACKGROUND,
                                           fg=settings.FAIL_COLOR,
                                           font=settings.SMALL_FONT)
                self.show_error.grid(row=1, columnspan=2)

    def sim_game(self, deck):
        ''' Simulates one game.'''
        # players_hands = hands
        free_cards = list(deck)
        board = []

        # Draw 5 board cards - 3 FLOP, 1 TURN, 1 RIVER.
        for _ in range(5):
            number = random.choice(free_cards)
            card = [(number - 1) // 13, (number - 1) % 13]
            board.append(card)
            free_cards.remove(number)
        
        # Show board cards.
        Board(self.parent, board).grid(row=1, columnspan=2, pady=(0,20))

        # Update board values for each Player object.
        for player in self.players_obj:
            player.board = board
            player.check_result()


    def validate_input(self, input):
        ''' Validates simulations amount input.'''
        try:
            value = int(input)
            if value < 1:
                self.error = 'Give an positive ingteger.'
            else:
                return value
        except ValueError:
            self.error = 'Invalid simulations amount value.'


    def sim_test(self):
        ''' For simulation algorithm testing. '''
        board = tests.sim_data[self.test_counter][2]
        Board(self.parent, board).grid(row=1, columnspan=2, pady=(0,20))
        results = []
        for player in self.players_obj:
            player_index = self.players_obj.index(player)
            player.board = board
            for card in player.cards:
                card_index = player.cards.index(card)
                card.current_card = tests.sim_data[self.test_counter][player_index][card_index]
                card.show_card(card.current_card)
            player.hand_update()
            player.check_result()
            results.append('{}: {}'.format(player.name, player.result))
        self.test_counter += 1

        for result in results:
            print(result)





class Board(tk.Frame):
    ''' 
        Frame containing 5 board cards - 3 flop cards, 1 turn card and 1 river card.
        Only used in single simulation mode.
    '''
    def __init__(self, parent, board):
        super().__init__(parent)
        self.parent = parent
        self.board = board

        self.config_frame()
        self.create_widgets()

    def config_frame(self):
        self['bg'] = settings.BACKGROUND

    def create_widgets(self):
        for card in self.board:
            if self.board.index(card) < 3:
                self.create_card(card).grid(row=0, column=self.board.index(card),
                                            padx=(10,0))
            else:
                self.create_card(card).grid(row=0, column=self.board.index(card),
                                            padx=(30,0))

    def create_card(self, card):
        ''' Returns card object.'''
        color = card[0]
        symbol = card[1]

        if symbol < 10:
            file_name = settings.IMG_DIR[1] + str(color) + '0' + str(symbol) + '.png'
        else:
            file_name = settings.IMG_DIR[1] + str(color) + str(symbol) +  '.png'
        img = ImageTk.PhotoImage(Image.open(file_name))

        card = tk.Label(self, image=img, bg=settings.BACKGROUND)
        card.image = img
        return card



# Other functions

def deck_populate():
    '''Populates CARD_DECK variable.'''
    for _ in range(4):
        settings.CARD_DECK.append(list(range(13))) 


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