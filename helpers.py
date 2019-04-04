# Classes and functions supporting main application.

import time
import queue
import pickle
import random
import glob, os
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from operator import itemgetter
from collections import Counter
import settings as stg # Application settings and constant variables.
if stg.TEST_MODE == True: import tests # For testing purpose

# TODO:
# * Check if parent variable is needed in those classes.
# * Remove original size images from repo?
# * Check if not better to set CARD_DECK as dictionary.
# * SUCCESS_COLOR


class MainWindow(tk.Frame):
    '''Container with widgets of pre simulation view.'''

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        deck_populate()
        self.config_frame()
        self.create_widgets()

    def config_frame(self):
        self['bg'] = stg.BACKGROUND
    
    def create_widgets(self):
        # Create players frames.
        self.players = []
        for _ in range(stg.PLAYER_MODE):
            self.players.append(Player(self, 'Player ' + str(_ + 1)))
        for index, player in enumerate(self.players):
            if index < len(self.players) - 1:
                player.grid(row=0, column=index, pady=(0,30), padx=(10,40))
            else: player.grid(row=0, column=index, pady=(0,30), padx=(10,10))
            
        # Simulation amount input frame.
        self.user_input = SimQuantity(self)
        self.user_input.grid(row=2, column=0, pady=(10,0))

        # Simulation button.
        self.sim_button = Simulate(self)
        self.sim_button.grid(row=2, column=1, pady=(10,0))
    
    def show_results(self, sim_amount):
        '''Changes main window to post simulation view.'''
        
        # Delete not needed widgets and show players results.
        self.user_input.grid_forget() # DESTROY?????
        self.sim_button.grid_forget() # DESTROY?????

        for player in self.players:
            player.post_sim(sim_amount)
        
        if sim_amount == 1:
            Board(self, self.players[0].board).grid(row=1, columnspan=2, pady=(0,20))
        
        # Button that allows to go back to pre simulation view, after seeing results.
        tk.Button(self, text='New Simulation', relief='flat', font=stg.FONT,
                  bg=stg.SUCCESS_COLOR, fg=stg.FOREGROUND,
                  highlightbackground=stg.BACKGROUND, highlightcolor=stg.BACKGROUND,
                  activebackground=stg.FOREGROUND, activeforeground=stg.BACKGROUND,
                  highlightthickness=2, command=self.parent.reset_view).grid(row=2,
                  columnspan=stg.PLAYER_MODE)
    


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
        self.board = [] # Current board cards.
        self.current_wins = 0
        self.win = False # For the sum up.
        
        self.config_frame()
        self.create_widgets()

    def config_frame(self):
        self['bg'] = stg.BACKGROUND
        self['fg'] = stg.FOREGROUND
        self['text'] = self.name
        self['font'] = stg.FONT

    def create_widgets(self):
        card_1 = Card(self)
        card_1.grid(row=0, column=0, pady=(10,10), padx=(10,15))
        card_2 = Card(self)
        card_2.grid(row=0, column=1, pady=(10,10), padx=(15,10))

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
        
        # Get colors and symbols from cards.
        for card in cards:
            colors.append(card[0])
            symbols.append(card[1])
        
        # Flush check.
        clr_counter = Counter(colors).most_common(1)
        if clr_counter[0][1] >= 5:
            self.result = 5 # stg.RESULTS[5] = Flush
            
            # Straight Flush check.
            if self.is_straight(symbols):
                self.result = 8
                return
       
        # Four of a kind check.
        smbl_counter = Counter(symbols).most_common(2)
        if smbl_counter[0][1] == 4:
            self.result = 7
            return
        
        # Three of a kind check.
        if smbl_counter[0][1] == 3:
            if not self.result:
                self.result = 3

            # Full house check.
            if smbl_counter[1][1] >= 2:
                self.result = 6
                return
        
        # Straight check.
        if not self.result or self.result < 4:
            if self.is_straight(symbols):
                self.result = 4
                return
        
        # Pair check.
        if not self.result: 
            if smbl_counter[0][1] == 2:
                self.result = 1

                # Two pair check.
                if smbl_counter[1][1] == 2:
                    self.result = 2
                    return
       
        # Else high card.
        if not self.result: self.result = 0
            
    def is_straight(self, symbols):
        ''' Check if given board contains straight. '''
        
        # Sort list and remove duplicates.
        straight_check = list(set(symbols))
        straight_check.sort()
        last_item = len(straight_check) - 1

        if len(straight_check) >= 5:
            # If ace is in the list, check for lower straight.
            if straight_check[last_item] == 12:
                lower_straight = list(straight_check)
                lower_straight[last_item] = -1
                lower_straight.sort()

                if lower_straight[4] - lower_straight[0] == 4: return True

            # Check other straight options.
            for _ in range(len(straight_check) - 4):
                if straight_check[4 + _] - straight_check[_] == 4: return True

        return False

    def post_sim(self, sim_amount):
        '''Show post simulation player view with result.'''

        # Hide not needed widgets from cards objects.
        for card in self.cards:
            for widget in card.changable_widgets:
                widget.grid_forget()
        
        # Show result.
        result_color = stg.FAIL_COLOR
        if sim_amount == 1:
            if self.current_wins == 1: result_color = stg.SUCCESS_COLOR
            tk.Label(self, text=stg.RESULTS[self.result], bg=self['bg'], fg=result_color,
                     font=stg.FONT).grid(row=1, columnspan=2, pady=(10,10))
        else:
            if self.win == True: result_color = stg.SUCCESS_COLOR
            win_rate = round(self.current_wins / sim_amount * 100, 2)
            tk.Label(self, text='WINNING RATE', bg=self['bg'], fg=result_color,
                     font=stg.FONT).grid(row=1, columnspan=2, pady=(10,0))
            tk.Label(self, text=str(win_rate) + '%', bg=self['bg'], fg=result_color,
                     font=stg.FONT).grid(row=2, columnspan=2, pady=(0,10))
            wins_display = f'{self.current_wins} / {sim_amount} GAMES'         
            tk.Label(self, text=wins_display, bg=self['bg'], fg=result_color,
                     font=stg.SMALL_FONT).grid(row=3, columnspan=2, pady=(0,10))
            


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
        self['bg'] = stg.BACKGROUND

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
            img = ImageTk.PhotoImage(Image.open(stg.IMG_DIR[0] + 'backside.png'))
        
        # Show current card.
        else:
            # Set file name to open.
            color = card[0]
            symbol = card[1]
            if symbol < 10:
                file_name = stg.IMG_DIR[0] + str(color) + '0' + str(symbol) + '.png'
            else:
                file_name = stg.IMG_DIR[0] + str(color) + str(symbol) +  '.png'
            img = ImageTk.PhotoImage(Image.open(file_name))
            
            # Update deck
            stg.CARD_DECK[color][symbol] = None

        card = tk.Label(self, image=img, bg=stg.BACKGROUND)
        card.image = img
        card.grid(row=0, columnspan=4, pady=(0,10))
        
    def create_radiobutton(self, img_name, val):
        '''Creates radiobutton with image as label. '''
        img = ImageTk.PhotoImage(Image.open(stg.IMG_DIR[0] + img_name + '.png'))
        button = tk.Radiobutton(self, image=img, bg=stg.BACKGROUND,
                                activebackground=stg.BACKGROUND, 
                                highlightthickness=0, variable=self.rbutton_option,
                                value=val, command=lambda: self.switch_color(val))
        button.image = img
        button.grid(row=1, column=val)
        return button

    def create_button(self, img_name, val, switcher):
        ''' Creates button as image.'''
        img = ImageTk.PhotoImage(Image.open(stg.IMG_DIR[0] + img_name + '.png'))
        button = tk.Button(self, image=img, bg=stg.BACKGROUND, bd=0,
                           activebackground=stg.BACKGROUND, highlightthickness=0,
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
                while(symbol > 12 or stg.CARD_DECK[color][symbol] == None):
                    # If outside card range, reset.
                    if symbol > 12: symbol = 0
                    else: symbol += 1
            # Look in negative drieciton.
            else:
                symbol -= 1
                while(symbol < 0 or stg.CARD_DECK[color][symbol] == None):
                    # If outside card range, reset backwards.
                    if symbol < 0: symbol = 12
                    else: symbol -= 1
            
            # Update current_card variable and show new card.
            self.current_card[0] = color
            self.current_card[1] = symbol
            self.show_card(self.current_card)
            stg.CARD_DECK[color][symbol] = None

    def update_deck(self, card):
        '''Deletes None value from CARD_DECK if card is not used anymore.'''
        if card[0] is not None and card[1] is not None:
            stg.CARD_DECK[card[0]][card[1]] = card[1]



class SimQuantity(tk.Frame):
    '''Gets user simulation amount input.'''

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.changable_widgets = []
        self.value = tk.StringVar()
        self.value.set(stg.DEFAULT_SIM_AMOUNT)

        self.config_frame()
        self.create_widgets()

    def config_frame(self):
        self['bg'] = stg.BACKGROUND

    def create_widgets(self):
        input_label = tk.Label(self, text='Simulations amount:', bg=stg.BACKGROUND, 
                               font=stg.FONT, fg=stg.FOREGROUND)
        input_entry = tk.Entry(self, textvariable=self.value, width=8, relief='flat',
                               bg=stg.BACKGROUND, fg=stg.FOREGROUND,
                               insertbackground=stg.SUCCESS_COLOR,
                               highlightbackground=stg.BACKGROUND,
                               highlightcolor=stg.BACKGROUND,
                               disabledbackground=stg.BACKGROUND, font=stg.FONT)
        input_label.grid(row=0, column=0)
        input_entry.grid(row=0,column=1)
        
        self.changable_widgets.append(input_label)
        self.changable_widgets.append(input_entry)



class Simulate(tk.Button):
    ''' Simulation algorithm and user input validadion.'''
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.players_obj = parent.players # Reference to players objects list.
        self.input_obj = parent.user_input # Reference to input object.
        self.show_error = None # Error label.

        self.widget_config()

    def widget_config(self):
        self['text'] = 'Simulate'
        self['relief'] = 'flat'
        self['font'] = stg.FONT
        self['bg'] = stg.SUCCESS_COLOR
        self['fg'] = stg.FOREGROUND
        self['highlightbackground'] = stg.BACKGROUND
        self['highlightcolor'] = stg.BACKGROUND
        self['activebackground'] = stg.FOREGROUND
        self['activeforeground'] = stg.BACKGROUND
        self['highlightthickness'] = 2
        self['command'] = lambda: self.simulate()
    
    def simulate(self):
        ''' Simulation algorithm.'''
        
        # Validate input.
        user_input = self.input_obj.value.get()
        self.sim_amount = self.validate_input(user_input)

        if self.sim_amount:
            stg.DEFAULT_SIM_AMOUNT = self.sim_amount
            # Set all the button and input widgets as disabled.
            for player in self.players_obj:
                for card in player.cards:
                    for widget in card.changable_widgets:
                        widget['state'] = 'disabled'
            for widget in self.input_obj.changable_widgets:
                widget['state'] = 'disabled'
            self['state'] = 'disabled'

            # Look for blank cards and remove already used cards.
            cards_to_random = []
            self.deck = list(range(1, 53))
            for player_object in self.players_obj:
                for card in player_object.cards:
                    if any(x is not None for x in card.current_card):
                        self.deck.remove(card.current_card[0] * 13 + 
                                         (card.current_card[1] + 1))
                    else:
                        cards_to_random.append(card)
            # If blank pick random card.
            for card in cards_to_random:
                random_card = random.choice(self.deck)
                card.current_card = [(random_card - 1) // 13, (random_card -1) % 13]
                card.show_card(card.current_card)
                self.deck.remove(random_card)
            
            # Update players hands.
            for player in self.players_obj:
                player.hand_update()
            
            # Simulate sim_amount of games.
            if self.sim_amount > 1:
                if not stg.TEST_MODE:
                    self.sim_thread()
                # Test mode.
                else:
                    for _ in range(self.sim_amount):
                        board = self.sim_test()
                        self.sim_game(board)
                        self.get_sim_winner()
                
            # Single game mode.
            else:
                if not stg.TEST_MODE: board = self.get_random_board()
                else: board = self.sim_test() # Test mode.
                self.sim_game(board)
                self.parent.show_results(self.sim_amount)

    def validate_input(self, input):
        ''' Validates simulations amount input. '''

        # Delete old error if exists.
        error = None
        if self.show_error:
            self.show_error.destroy()
        try:
            value = int(input)
            if value < 1:
                error = 'Give a positive integer.'
        except ValueError:
            error = 'Invalid simulations amount value.'

        if error:
            self.show_error = tk.Label(self.parent, text=error, bg=stg.BACKGROUND,
                                       fg=stg.FAIL_COLOR, font=stg.SMALL_FONT)
            self.show_error.grid(row=1, columnspan=2)
        else:
            return value
    
    def sim_thread(self):
        '''Simulates sim_amount of games, if needed in different thread.'''

        sim_time = self.get_sim_time()
        
        # If simulation is longer than a few seconds, create thread and progress bar.
        if sim_time > 2:
            self.stop_sim = threading.Event()
            prog_bar = ProgressBar(self.parent, self.stop_sim)
            prog_bar.grid(row=1, columnspan=2, pady=(10,20))
            self.parent.update()
            
            prog_status = queue.LifoQueue()
            t = threading.Thread(target=self.sim_n_games, daemon=True, args=(prog_status,))
            t.start()
            self.check_progress(prog_status, prog_bar)

        # For short simulation additional thread is not needed.
        else:
            self.parent.update()
            self.sim_n_games()
            self.get_sim_winner()
        
    def get_sim_time(self):
        '''Returns time needed for sim_amount of simulations.'''

        # Get average simulaton time value.
        try:
            with open('data.pickle', 'rb') as f:
                stg.DATA = pickle.load(f)
                avg_sim_time = stg.DATA.get('avg_sim_time')
        except FileNotFoundError:
            # Make some initial simulations.
            tests_amount = 100
            start = time.time()
            for _ in range(tests_amount):
                board = self.get_random_board()
                self.sim_game(board)
            end = time.time()
            avg_sim_time = (end - start) / tests_amount
            stg.DATA['avg_sim_time'] = avg_sim_time
            with open('data.pickle', 'wb') as f:
                pickle.dump(stg.DATA, f)
        
        return avg_sim_time * self.sim_amount

    def check_progress(self, prog_status, prog_bar):
        '''Checks current progress queue status and updates progress bar.'''
        if not prog_status.empty():
            message = prog_status.get()
            if message is 'DONE': 
                prog_bar.destroy_widgets()
                self.get_sim_winner()
                return
            elif message is 'ABORT':
                self.parent.parent.reset_view()
                return
            prog_bar.bar['value'] = message
            
        self.parent.parent.after(200, self.check_progress, prog_status, prog_bar)
            
    def sim_n_games(self, status=None):
        '''Simulates n number of games and measures simulation time.'''
        
        start = time.time()
        # Simulation with progress bar.
        if status:
            # Assess interval of information progress update.
            interval = self.sim_amount // 100
            rest_sim = self.sim_amount % 100
            for sim_percent in range(100):
                for _ in range(interval):
                    board = self.get_random_board()
                    self.sim_game(board)
                status.put(sim_percent + 1)
                if self.stop_sim.is_set():
                    status.put('ABORT')
                    return
            # Simulate rest of the games.
            for _ in range(rest_sim):
                board = self.get_random_board()
                self.sim_game(board)
            status.put('DONE')
        
        # Simulation without progress bar.
        else:
            for _ in range(self.sim_amount):
                board = self.get_random_board()
                self.sim_game(board)
        end = time.time()
        
        # Get the simulation time and update data file.
        sim_time = (end - start) / self.sim_amount
        stg.DATA['avg_sim_time'] = (stg.DATA['avg_sim_time'] + sim_time) / 2
        with open('data.pickle', 'wb') as f:
            pickle.dump(stg.DATA, f)

    def get_sim_winner(self):
        '''Looks for the players with the best general scores and shows score window.'''

        winners = []
        for player in self.players_obj:
            if winners:
                if winners[0].current_wins < player.current_wins:
                    winners = []
                    winners.append(player)
                elif winners[0].current_wins == player.current_wins:
                    winners.append(player)
            else: winners.append(player)
        
        for winner in winners: winner.win = True
        self.parent.show_results(self.sim_amount)

    def get_random_board(self):
        '''Returns five random board cards.'''

        free_cards = list(self.deck)
        board = []

        for _ in range(5):
            number = random.choice(free_cards)
            card = [(number - 1) // 13, (number - 1) % 13]
            board.append(card)
            free_cards.remove(number)

        return board

    def sim_game(self, board):
        ''' Simulates one game.'''
        
        # Update board values and look for results.
        for player in self.players_obj:
            player.board = board
            player.check_result()

        winners = self.win_check()

        # Check and assign winners.
        for player in self.players_obj:
            for winner in winners:
                if player == winner:
                    player.current_wins += 1
                    winners.remove(winner)
                    break

    def win_check(self):
        '''Returns list of winner/winners.'''
        winner = []
        for player in self.players_obj:
            if winner:
                if winner[0].result < player.result:
                    winner = []
                    winner.append(player)
                elif winner[0].result == player.result:
                    better_card = self.players_compare(winner[0], player)
                    if not better_card:
                        winner.append(player)
                    elif winner[0] != better_card:
                        winner = []
                        winner.append(player)
            else: winner.append(player)
        return winner

    def players_compare(self, player_a, player_b):
        ''' Returns player object with better hand. If hands are even, returns None. '''

        cards_a = sorted(player_a.hand + player_a.board, key=itemgetter(1))
        cards_b = sorted(player_b.hand + player_b.board, key=itemgetter(1))
        result = player_a.result
        symbols_a = []
        symbols_b = []
        colors_a = []
        colors_b = []

        for _ in range(7):
            symbols_a.append(cards_a[_][1])
            symbols_b.append(cards_b[_][1])
            colors_a.append(cards_a[_][0])
            colors_b.append(cards_b[_][0])
        
        # High card.
        if result == 0:
            for _ in range(5):
                if cards_a[6-_][1] > cards_b[6-_][1]:
                    return player_a
                elif cards_a[6-_][1] < cards_b[6-_][1]:
                    return player_b
            return None

        # One pair.
        if result == 1:
            pair_a = Counter(symbols_a).most_common(1)[0][0]
            pair_b = Counter(symbols_b).most_common(1)[0][0]
            # Look for best player.
            if pair_a > pair_b: return player_a
            elif pair_a < pair_b: return player_b
            else:
                # Players have the same pair, look for higher card.
                # Remove pairs from player boards.
                self.card_remove([pair_a, pair_b],[cards_a, cards_b])
                # Look for higher card.
                for _ in range(3):
                    if cards_a[4-_][1] > cards_b[4-_][1]: return player_a
                    elif cards_a[4-_][1] < cards_b[4-_][1]: return player_b
                return None

        # Two pairs.
        if result == 2:
            # Lists of most common cards.
            common_a = Counter(symbols_a).most_common(3)
            common_b = Counter(symbols_b).most_common(3)
            pairs_a = []
            pairs_b = []
            for _ in range(3):
                if common_a[2-_][1] == 2: pairs_a.append(common_a[2-_][0])
                if common_b[2-_][1] == 2: pairs_b.append(common_b[2-_][0])
            # Select two highest pairs possible for each player.
            pairs_a.sort(reverse=True)
            pairs_a = pairs_a[:2]
            pairs_b.sort(reverse=True)
            pairs_b = pairs_b[:2]
            # Look for better player.
            if pairs_a[0] > pairs_b[0] or pairs_a[1] > pairs_b[1]: return player_a
            elif pairs_a[0] < pairs_b[0] or pairs_a[1] < pairs_b[1]: return player_b
            else:
                # Both players have the same pairs. Look for kicker.
                # Remove pairs from card sets.
                self.card_remove([pairs_a[0],pairs_b[0]], [cards_a, cards_b])
                self.card_remove([pairs_a[1],pairs_b[1]], [cards_a, cards_b])
                if cards_a[2][1] > cards_b[2][1]: return player_a
                elif cards_a[2][1] < cards_b[2][1]: return player_b
                else: return None

        # Three of a kind.
        if result == 3:
            # Look for the higher set/trips.
            set_a = Counter(symbols_a).most_common(1)[0][0]
            set_b = Counter(symbols_b).most_common(1)[0][0]
            if set_a > set_b: return player_a
            elif set_a < set_b: return player_b
            # Else players have even sets. Look for the kicker.
            else:
                self.card_remove([set_a, set_b], [cards_a, cards_b])
                for _ in range(2):
                    if cards_a[3-_][1] > cards_b[3-_][1]: return player_a
                    elif cards_a[3-_][1] < cards_b[3-_][1]: return player_b
                return None
        
        # Straight.
        if result == 4:
            straight_a = None
            straight_b = None
            # Look for highest straight.
            for _ in range(3):
                if straight_a is None and symbols_a[6-_] - symbols_a[2-_] == 4:
                    straight_a = symbols_a[2-_:7-_]
                if straight_b is None and symbols_b[6-_] - symbols_b[2-_] == 4:
                    straight_b = symbols_b[2-_:7-_]
            # If any of straights are still None, than it must be a lower straight.
            if straight_a is None or straight_b is None:
                if straight_a is not None and straight_b is None: return player_a
                elif straight_a is None and straight_b is not None: return player_b
                else: return None
            
            if straight_a > straight_b: return player_a
            elif straight_a < straight_b: return player_b
            else: return None
        
        # Flush.
        if result == 5:
            # There can be only one color, so check only 1 player.
            color = Counter(colors_a).most_common(1)[0][0]
            # Remove no color cards and look for highest color card.
            self.card_remove(color, [cards_a, cards_b], 'color')
            size_a = len(cards_a) - 1
            size_b = len(cards_b) - 1 
            for _ in range(5):
                if cards_a[size_a-_][1] > cards_b[size_b-_][1]: return player_a
                elif cards_a[size_a-_][1] < cards_b[size_b-_][1]: return player_b
            return None
        
        # Full house.
        if result == 6:
            # List most common cards and assign to pairs or sets.
            common_a = Counter(symbols_a).most_common(3)
            common_b = Counter(symbols_b).most_common(3)
            # Look for the highest three of a kind.
            set_a, set_b = common_a[0][0], common_b[0][0]
            if common_a[1][1] == 3 and set_a < common_a[1][0]:
                set_a = common_a[1][0]
                common_a.remove(common_a[1])
            else: common_a.remove(common_a[0])
            if common_b[1][1] == 3 and set_b < common_b[1][0]:
                set_b = common_b[1][0]
                common_b.remove(common_b[1])
            else: common_b.remove(common_b[0])
            # Look for the highest pairs.
            pair_a, pair_b = common_a[0][0], common_b[0][0]
            if common_a[1][1] >= 2 and pair_a < common_a[1][0]: pair_a = common_a[1][0]
            if common_b[1][1] >= 2 and pair_b < common_b[1][0]: pair_b = common_b[1][0]
            # Check which player is better.
            if set_a > set_b: return player_a
            elif set_a < set_b: return player_b
            elif pair_a > pair_b: return player_a
            elif pair_a < pair_b: return player_b
            else: return None
        
        # Four of a kind.
        if result == 7:
            # Get four of a kind symbol and remove from decks.
            common = Counter(symbols_a).most_common(1)[0][0]
            self.card_remove([common, common], [cards_a, cards_b])
            # Check which player is better.
            if cards_a[2][1] > cards_b[2][1]: return player_a
            elif cards_a[2][1] < cards_b[2][1]: return player_b
            else: return None
        
        # Straight Flush.
        if result == 8:
            # Remove all non color cards from decks and look for highest color card.
            color = Counter(colors_a).most_common(1)[0][0]
            self.card_remove(color, [cards_a, cards_b], 'color')
            symbols_a, symbols_b = [], []
            size_a, size_b = len(cards_a) - 1, len(cards_b) - 1
            highest_a, highest_b = None, None
            # Add symbols in color to the lists.
            for _ in range(7):
                if _ <= size_a:
                    symbols_a.append(cards_a[_][1])
                if _ <= size_b:
                    symbols_b.append(cards_b[_][1])
            # Look for the highest symbol in straight flush.
            for _ in range(3):
                if (highest_a == None and 
                    5 + _ <= size_a + 1 and
                    symbols_a[size_a-_] - symbols_a[size_a-4-_] == 4):
                    highest_a = symbols_a[size_a-_]
                if (highest_b == None and
                    5 + _ <= size_b + 1 and
                    symbols_b[size_b-_] - symbols_b[size_b-4-_] == 4):
                    highest_b = symbols_b[size_b-_]
            
            # If any highest cards are None, it must be a lower straight flush.
            if highest_a is None or highest_b is None:
                if highest_a is not None and highest_b is None: return player_a
                elif highest_a is None and highest_b is not None: return player_b
                else: return None
                
            if highest_a > highest_b: return player_a
            elif highest_a < highest_b: return player_b
            else: return None

    def card_remove(self, cards, boards, mode='symbol'):
        ''' Removes given cards, from given boards. '''
        iterator_a = 0
        iterator_b = 0

        while iterator_a < len(boards[0]) and iterator_b < len(boards[1]):
            # Remove card from Player A deck, if it matches given symbol.
            if mode == 'symbol' and cards[0] == boards[0][iterator_a][1]:
                boards[0].remove(boards[0][iterator_a])
            # Remove card from Player A deck, that is not in given color.
            elif mode == 'color' and cards != boards[0][iterator_a][0]:
                boards[0].remove(boards[0][iterator_a])
            else: iterator_a += 1
            
            # Remove card from Player B deck, if it matches given symbol.
            if mode == 'symbol' and cards[1] == boards[1][iterator_b][1]:
                boards[1].remove(boards[1][iterator_b])
            # Remove card from Player A deck, that is not in given color.
            elif mode == 'color' and cards != boards[1][iterator_b][0]:
                boards[1].remove(boards[1][iterator_b])
            else: iterator_b += 1

    def sim_test(self):
        '''Returns board and sets player cards from tests.py.'''
        # Get board cards from tests.py.
        board = tests.sim_data[stg.TEST_COUNTER][2]
        # Get player cards from test.py.
        for player in self.players_obj:
            player_index = self.players_obj.index(player)
            for card in player.cards:
                card_index = player.cards.index(card)
                card.current_card = tests.sim_data[stg.TEST_COUNTER][player_index][card_index]
                card.show_card(card.current_card)
            player.hand_update()
        stg.TEST_COUNTER += 1

        return board



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
        self['bg'] = stg.BACKGROUND

    def create_widgets(self):
        for index, card in enumerate(self.board):
            if index < 3: self.create_card(card).grid(row=0, column=index, padx=(10,0))
            else: self.create_card(card).grid(row=0, column=index, padx=(30,0))

    def create_card(self, card):
        ''' Returns card object. '''
        color = card[0]
        symbol = card[1]

        if symbol < 10:
            file_name = stg.IMG_DIR[1] + str(color) + '0' + str(symbol) + '.png'
        else:
            file_name = stg.IMG_DIR[1] + str(color) + str(symbol) +  '.png'
        img = ImageTk.PhotoImage(Image.open(file_name))

        card = tk.Label(self, image=img, bg=stg.BACKGROUND)
        card.image = img
        return card



class ProgressBar(tk.Frame):
    '''Frame containing Progressbar and Abort button.'''

    def __init__(self, parent, abort):
        super().__init__(parent)
        self.parent = parent
        self.abort = abort

        self.config_frame()
        self.create_widgets()

    def config_frame(self):
        self['bg']= stg.BACKGROUND
    
    def create_widgets(self):
        # Progress bar.
        bar_style = ttk.Style()
        bar_style.configure('Horizontal.TProgressbar', thickness=5,
                            troughcolor=stg.FOREGROUND, troughrelief='flat',
                            borderwidth=2, pbarrelief='flat')
        self.bar = ttk.Progressbar(self, style='Horizontal.TProgressbar',
                                   orient='horizontal', length=300, mode='determinate')
        self.bar.grid(row=0, column=0)

        # Button.
        img = ImageTk.PhotoImage(Image.open(stg.IMG_DIR[0] + 'abort.png'))
        self.button = tk.Button(self, image=img, bg=stg.BACKGROUND, bd=0,
                           activebackground=stg.BACKGROUND, highlightthickness=0,
                           command=self.stop_sim)
        self.button.image = img
        self.button.grid(row=0, column=1, padx=(10,0))
    
    def stop_sim(self):
        self.abort.set()

    def destroy_widgets(self):
        self.bar.destroy()
        self.button.destroy()



# Other functions
def deck_populate():
    ''' Populates CARD_DECK variable. '''
    stg.CARD_DECK = []
    for _ in range(4):
        stg.CARD_DECK.append(list(range(13))) 

def card_resize(scale, path, save_path):
    ''' Script helping to resize original card images. '''
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