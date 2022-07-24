"""
Casino program that I made for my own use.
It was created to try and learn how to use the MySQL database.
"""

from random import choice, randint, shuffle
from inspect import cleandoc
from time import sleep
import sys
import mysql.connector
import cryptocode
import SQL_VARS
from Crypto_key import KEY
import os


class Casino:
    """
    Casino class.
    """

    def __init__(self):
        self.username = ""
        self.balance = 0
        self.user_id = 0

    def login_menu(self):
        """
        Function for the login menu.
        You have the option to register, login, or exit.
        """
        menu = """
                Welcome to the casino!
                Do you want to login or register?
                1: Login.
                2: Register.
                3: Exit.
                """
        while True:
            os.system("cls")
            print(cleandoc(menu))
            # Loop until user enters a valid guess.
            guess = input("Enter your guess: ")
            if guess == "1":
                Casino.login(self)

            elif guess == "2":
                Casino.register()

            elif guess == "3":
                break

    @staticmethod
    def register():
        """
        Function to register a new user.
        The password will be encrypted and store in the SQL server with the username.
        Balance will be set to 1000 as default.
        """
        print("\n"*5)
        # Register a new user.
        print("Please register")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")

        # Check if username is already taken.
        if not Casino.check_username(username):
            sleep(2)
            return

        if not Casino.check_password(password, confirm_password):
            sleep(2)
            return

        # Get user_id by len of user_id length.
        cursor.execute("SELECT * FROM user_table")
        user_id = len(cursor.fetchall())

        # Insert new user into database.
        query = "INSERT INTO user_table (username, password, balance, user_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(
            query, (username, cryptocode.encrypt(password, KEY), 1000, user_id))
        conn.commit()
        print("User registered!")

    def login(self):
        """
        Function to login.
        First check if the username is in the database.
        Then decrypt the password assosiated with the username.
        Check if it matches the password the user entered.
        Next set the username, user_id, and balance to the class variables.
        """
        while True:
            print("\n"*5)
            print("Please login")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            # Find username in database.
            query = "SELECT * FROM user_table WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            # If username is not found.
            if user is None:
                print("User or/and password is incorrect!")
                sleep(2)
                return

            # Compare inputted password with the password in the database.
            if password != cryptocode.decrypt(user[1], KEY):
                print("User or/and password is incorrect!")
                sleep(2)
                return

            # If username and password is correct.
            self.username = username
            self.balance = user[2]
            self.user_id = user[3]
            break

        Casino.main_menu(self)

    def main_menu(self):
        """
        Main menu.
        Here you can choose what you want to do.
        """
        game_menu = """
            1: Scratch card.
            2: Roulette.
            3: Blackjack.
            4: Dices.
            5: Settings.
            6: Exit.
            """
        while True:
            print("\n"*5)
            self.balance = Casino.read_balance(self)
            print(f"Hello {self.username}! Your balance is ${self.balance}")
            print(cleandoc(game_menu))
            guess = input("Enter your guess: ")
            if guess == "1":
                Casino.scratch_card(self)

            elif guess == "2":
                Casino.roulette(self)

            elif guess == "3":
                Casino.blackjack()

            elif guess == "4":
                Casino.dices(self)

            elif guess == "5":
                Casino.settings(self)

            elif guess == "6":
                break

    def scratch_card(self):
        """
        Scratch card.
        Here you can choose if you want to play, read the rules or go back.
        The symbols are randomly generated.
        If the symbols line up you win.
        Depening on the how many symbols line up the multiplier will differ.
        """
        while True:
            print("\n"*5)
            print("1: Place bet.\n2: Rules.\n3: Exit.")
            guess = input("Enter your guess: ")
            if guess == "1":
                # Place bet.
                bet = Casino.bet_func(self)
                # Symbols for the scratch card.
                symbols = ["♠", "♥", "♦", "♣"]
                # Get random symbol 4 times in different variables.
                symbol1 = symbols[randint(0, 3)]
                symbol2 = symbols[randint(0, 3)]
                symbol3 = symbols[randint(0, 3)]
                symbol4 = symbols[randint(0, 3)]
                print(f"Your card is: {symbol1}{symbol2}{symbol3}{symbol4}")
                # Check if symbols line up.
                # If XXXX.
                if symbol1 == symbol2 and symbol2 == symbol3 and symbol3 == symbol4:
                    Casino.bet_won(self, bet, 50)
                    continue

                # If XXYY.
                if symbol1 == symbol2 and symbol3 == symbol4:
                    Casino.bet_won(self, bet, 10)
                    continue

                # If XXXY.
                if symbol1 == symbol2 and symbol2 == symbol3:
                    Casino.bet_won(self, bet, 5)
                    continue

                # If XXYZ
                if symbol1 == symbol2:
                    Casino.bet_won(self, bet, 1)
                    continue

                # If none of the above.
                Casino.bet_lost(bet)

            elif guess == "2":
                rules = """Rules for scratch cards:
                Place a bet and you will receive a scratchcard.
                The scratchcard will have 4 symbols.
                If you have the same symbols, you will win 50 times your bet.
                If you have 3 of the same symbols, you will win 25 times your bet.
                If you have 2 of the same symbols, you will win 0.5 times your bet."""
                print(cleandoc(rules))

            elif guess == "3":
                return

            sleep(2)

    def roulette(self):
        """
        Play roulette.
        Here you can choose if you want to play, read the rules or go back.
        First you guess what number it will be.
        Then the roulette will "spin" (randomly generate a number).
        If you guess the right number you win 36x your bet.
        """
        while True:
            print("\n"*5)
            print("1: Place bet.\n2: Rules.\n3: Exit.")
            guess = input("Enter your guess: ")
            if guess == "1":
                # Place bet.
                bet = Casino.bet_func(self)
                while True:
                    # Get number from user.
                    guess = input("Enter the number: ")
                    # Check if guess is a number.
                    if guess.isdigit():
                        guess = int(guess)
                        break
                    print("Invalid number!\n The number has to be between 0 and 36.")

                # Get random number.
                number = randint(0, 36)
                print(f"The number is: {number}! You guessed {guess}!")
                # If the guess is correct.
                if number == guess:
                    Casino.bet_won(self, bet, 36)
                    continue

                # If the guess is incorrect.
                Casino.bet_lost(bet)

            elif guess == "2":
                rules = """Rules for roulette:
                Place a bet and you will receive a roulette.
                The roulette will have 36 numbers.
                If you guess the number, you will receive your bet multiplied by 36."""
                print(cleandoc(rules))

            elif guess == "3":
                break

            sleep(2)

    def blackjack(self):
        """
        Play blackjack.
        """
        while True:
            print("\n"*5)
            print("1: Place bet.\n2: Rules.\n3: Exit.")
            guess = input("Enter your guess: ")
            print("\n"*5)
            if guess == "1":
                # Place bet.
                bet = Casino.bet_func(self)

                # Create deck.
                values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
                          'Queen': 10, 'King': 10, 'Ace': 11}
                playing = True

                # Create a deck of cards.
                class Deck:
                    def __init__(self):
                        suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
                        ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
                                 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
                        self.deck = []  # start with an empty list#
                        for suit in suits:
                            for rank in ranks:
                                self.deck.append(Card(suit, rank))

                    def __str__(self):
                        deck_comp = ''  # strating competition deck empty#
                        for card in self.deck:
                            deck_comp += '\n' + card.__str__()  # add each card object;s strin#
                        return 'The deck has' + deck_comp

                    def shuffle(self):
                        shuffle(self.deck)

                    def deal(self):
                        single_card = self.deck.pop()
                        return single_card

                # Create a card class.
                class Card:
                    def __init__(self, suit, rank):
                        self.suit = suit
                        self.rank = rank

                    def __str__(self):
                        return self.rank + ' of ' + self.sui

                class Hand:
                    def __init__(self):
                        self.cards = []  # start with an empty list as we did in the Deck class
                        self.value = 0   # start with zero value
                        self.aces = 0    # add an attribute to keep track of aces

                    # Here we add cards to the hand.
                    def add_card(self, card):
                        self.cards.append(card)
                        self.value += values[card.rank]
                        if card.rank == 'Ace':
                            self.aces += 1

                    # Here we check if the hand has an ace and if it does, check if it can be reduced to a 1.
                    def adjust_for_ace(self):
                        while self.value > 21 and self.aces:
                            self.value -= 10
                            self.aces -= 1

                # Hit - take another card.
                def hit(deck, hand):
                    hand.add_card(deck.deal())
                    hand.adjust_for_ace()

                # Func for hit or stand.
                def hit_or_stand(deck, hand):
                    global playing
                    while True:
                        x = input("Would you like to [h]it or [s]tand?\n")
                        if x.lower() == 'h' or x.lower() == 'hit':
                            hit(deck, hand)  # hit() function defined above
                        elif x.lower() == 's' or x.lower() == 'stand':
                            print("Player stands. Dealer is playing.")
                            sleep(1)
                            playing = False
                        else:
                            print("Sorry, please try again.")
                            continue
                        break

                # Show cards.
                def show_some(player, dealer):
                    print("\n"*5)
                    dealer_hand = f""" 
                    Dealer's Hand:
                    {dealer.cards[0]}
                    <Hidden card>
                    Value: {values.get(dealer.cards[0].rank)}
                    """

                    print(cleandoc(dealer_hand))
                    print("\n")
                    print("Player's Hand: ", *player.cards, sep='\n')
                    print(f"Value: {player.value}")
                    sleep(2)

                # Show all cards.
                def show_all(player, dealer):
                    print("\n"*5)
                    print("Dealer's Hand: ", *dealer.cards, sep='\n')
                    print(f"Value: {dealer.value}")
                    print("\n")
                    print("Player's Hand: ", *player.cards, sep='\n')
                    print(f"Value: {player.value}")
                    print("\n")
                    sleep(2)

                while True:
                    # Create & shuffle the deck, deal two cards to each player
                    deck = Deck()
                    deck.shuffle()

                    player_hand = Hand()
                    player_hand.add_card(deck.deal())
                    player_hand.add_card(deck.deal())

                    dealer_hand = Hand()
                    dealer_hand.add_card(deck.deal())
                    dealer_hand.add_card(deck.deal())

                    # Show cards (but keep one dealer card hidden)
                    show_some(player_hand, dealer_hand)

                    while playing:  # recall this variable from our hit_or_stand function
                        sleep(2)
                        # Prompt for Player to Hit or Stand
                        hit_or_stand(deck, player_hand)

                        # Show cards (but keep one dealer card hidden)
                        show_some(player_hand, dealer_hand)

                        # If player's hand exceeds 21, run player_busts() and break out of loop
                        if player_hand.value > 21:
                            Casino.bet_lost(self)
                            break

                        if player_hand.value == 21:
                            Casino.bet_won(self, bet, 2)
                            break

                        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
                        if player_hand.value < 21:
                            while dealer_hand.value < 17:
                                sleep(2)
                                hit(deck, dealer_hand)

                            # Show all cards
                            show_all(player_hand, dealer_hand)

                            # Run different winning scenarios
                            if dealer_hand.value > 21:
                                Casino.bet_won(self, bet, 2)
                                break

                            elif dealer_hand.value > player_hand.value:
                                Casino.bet_lost(self)
                                break

                            elif dealer_hand.value < player_hand.value:
                                Casino.bet_won(self, bet, 2)
                                break

                            else:
                                Casino.bet_won(self, bet, 1)
                                break
                    break

            if guess == "2":
                """
                Blackjack rules.
                The goal of the game is to get as close to 21 as possible without going over.
                The game begins with two cards dealt to each player.
                The player can then choose to either hit or stand.
                If the player hits and exceeds 21, the player is bust and loses.
                If the player stands, the dealer will take his turn.
                The dealer will hit until his hand exceeds 17.
                If the dealer busts, the player wins.
                """
            if guess == "3":
                break

    def dices(self):
        """
        Roll dices.
        First you can choose what you want to do. Play, read the rules or go back.
        When playing you roll 2 dices and if the dices are the same number you win.
        You win 6x your bet.
        """
        while True:
            print("\n"*5)
            print("1: Place bet.\n2: Rules.\n3: Exit.")
            guess = input("Enter your guess: ")
            if guess == "1":
                # Place bet.
                bet = Casino.bet_func(self)
                dice1 = randint(1, 6)
                dice2 = randint(1, 6)
                print(f"Dice 1: {dice1}\nDice 2: {dice2}")
                # If d1 and d2 are equal.
                if dice1 == dice2:
                    Casino.bet_won(self, bet, 6)
                    continue
                # If d1 and d2 are not equal.
                Casino.bet_lost(bet)

            elif guess == "2":
                rules = """Rules for dices:
                Place a bet and roll the dice!
                If you roll the same number, you will win 6 times your bet."""
                print(cleandoc(rules))

            elif guess == "3":
                break

        sleep(2)

    def coinflip(self):
        """
        Coinflip.
        """
        while True:
            print("\n"*5)
            print("1: Place bet.\n2: Rules.\n3: Exit.")
            guess = input("Enter your guess: ")
            if guess == "1":
                # Place bet.
                bet = Casino.bet_func(self)
                while True:
                    # Get number from user.
                    guess = input("Enter heads or tails: ")
                    # Check if guess is a number.
                    if guess.lower() == "heads" or guess.lower() == "tails":
                        break
                    print("Invalid input!\n The input has to be heads or tails.")

                # If number is 0.
                if choice(["heads", "tails"]) == guess:
                    Casino.bet_won(self, bet, 2)
                    continue

                # If number is 1.
                Casino.bet_lost(bet)

            elif guess == "2":
                rules = """Rules for coinflip:
                Place a bet and you will receive a coinflip.
                The coinflip will have 2 numbers.
                If you guess the number, you will win 2x of your bet."""
                print(cleandoc(rules))

            elif guess == "3":
                break

            sleep(2)

    def settings(self):
        """
        Settings.
        Here you can change your username, password, reset your balance or go back.
        When changing your username check if already exists and if isn't current username.
        When changing your password it will be encrypted and saved in the database.
        Reset balance can be used if you dont have any money left.
        """
        while True:
            print("\n"*5)
            print("1: Change username.\n2: Change password.\n3: Reset Balance.\n4: Exit.")
            guess = input("Enter your guess: ")
            if guess == "1":
                new_username = input("Enter your new username: ")
                if Casino.change_username(self, new_username) is not None:
                    self.username = new_username
                    print("Your username has been changed!")

            elif guess == "2":
                # Change password.
                new_password = input("Enter your new password: ")
                confirm_password = input("Confirm your new password: ")
                if Casino.change_password(self, new_password, confirm_password) is not None:
                    print("Your password has been changed!")

            elif guess == "3":
                # Reset balance.
                new_balance = 1000
                try:
                    # Change the balance.
                    query = "UPDATE users SET balance = %s WHERE user_id = %s"
                    cursor.execute(query, (new_balance, self.user_id))
                    conn.commit()
                except mysql.connector.Error:
                    print("Something went wrong! Balance has been updated locally.")
                    self.balance = new_balance
                    continue
                print("Your balance has been reset!")

            elif guess == "4":
                return

            sleep(2)

    def bet_func(self):
        """
        Function to do the betting.
        First the script will get the latest balance from the database for the user.
        Then it will ask for the amount of the bet.
        The amount the suer wants to bet goes through the check_bet function.
        If check_bet returns True, the balance will be updated in the database.
        And the amount of the bet will be returned.
        """
        while True:
            # Read the balance.
            self.balance = Casino.read_balance(self)
            # Check for valid input
            try:
                bet = int(input("Enter your bet: "))
            except ValueError:
                print("Invalid guess.")
                continue

            # Check if the bet is valid.
            if not Casino.check_bet(self, bet):
                continue

            # Update the balance.
            new_balance = self.balance - bet
            try:
                # Update the balance.
                query = "UPDATE users SET balance = %s WHERE user_id = %s"
                cursor.execute(query, (new_balance, self.user_id))
                conn.commit()
            except mysql.connector.Error:
                self.balance = new_balance
            return bet

    def check_bet(self, bet):
        """
        Check if the bet is valid.
        The bet can't be higher than the balance.
        The bet can't be 0 or lower.
        """
        # Check if the bet isnt bigger than the balance.
        if bet > self.balance:
            print("You don't have enough money!")
            return False

        # Check if the bet isnt 0.
        if bet == 0:
            print("You can't bet 0!")
            return False

        # Check if the bet isnt negative.
        if bet < 0:
            print("You can't bet a negative number!")
            return False
        return True

    def bet_won(self, bet, multiplier):
        """
        Function for if bet was won.
        First the balance is read from the database.
        Then the balance and database is updated with the amount of the bet.
        """
        # Read the balance.
        self.balance = Casino.read_balance(self)
        print(f"You won ${bet * multiplier}!")
        # Multiply the bet by the multiplier and add to balance.
        new_balance = self.balance + (bet * multiplier)
        try:
            # Update the balance in SQL.
            query = "UPDATE users SET balance = %s WHERE user_id = %s"
            cursor.execute(query, (new_balance, self.user_id))
            conn.commit()
        except mysql.connector.Error:
            print("Something went wrong! Balance has been updated locally.")
            self.balance = new_balance

    @staticmethod
    def bet_lost(bet):
        """
        Function for if bet was lost.
        """
        print(f"You lost ${bet}!")

    def read_balance(self):
        """
        Function to read the balance from the database.
        Send query to the SQL database with the user_id.
        Return the received balance.
        """
        try:
            # Read the balance from SQL and return it.
            query = "SELECT balance FROM user_table WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            return cursor.fetchone()[0]
        except mysql.connector.Error:
            return self.balance

    def change_username(self, new_username):
        """
        Function to change the username.
        First check the username in the check_username function.
        If the username is valid, send query to the SQL database with the new username.
        Return the new username.
        """
        # Check if username already exists.
        if not Casino.check_username(new_username):
            return None

        # Change the username.
        try:
            query = "UPDATE users SET username = %s WHERE user_id = %s"
            cursor.execute(query, (new_username, self.user_id))
            conn.commit()
        except mysql.connector.Error:
            print("Something went wrong!")
            return None
        return new_username

    def change_password(self, new_password, confirm_password):
        """
        Function to change the password.
        First check the password in the check_password function.
        Then encrypt the password.
        Then send query to the SQL database with the new password.
        Return the new password.
        """
        # Check if the password is valid.
        if not Casino.check_password(new_password, confirm_password):
            return None
        # Encrypt the password.
        new_password = cryptocode.encrypt(new_password, KEY)

        # Change the password.
        try:
            query = "UPDATE users SET password = %s WHERE user_id = %s"
            cursor.execute(query, (new_password, self.user_id))
            conn.commit()
        except mysql.connector.Error:
            print("Something went wrong!")
            return None
        return new_password

    @staticmethod
    def check_username(username):
        """
        Function to check if the username is already in the database.
        First check if username is longer than 3 characters.
        Then send query to the SQL database with the username.
        Return True if username is not in the database.
        """
        if len(username) < 3:
            print("Username is too short!")
            return False
        try:
            query = "SELECT * FROM user_table WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            if user is not None:
                print("Username is already taken!")
                return False
        except mysql.connector.Error:
            print("Something went wrong!")
            return False
        return True

    @staticmethod
    def check_password(password, confirm_password):
        """
        Function to check if the password is valid.
        """
        # Check if the password matches the confirm password.
        if password != confirm_password:
            print("Passwords don't match!")
            return False

        if len(password) < 5:
            print("Password must be at least 5 characters long!")
            return False

        if not any(char.isdigit() for char in password):
            print('Password should have at least one numeral')
            return False
        return True


def connection():
    """
    Connect to the database.
    Try to connect to the database.
    If it fails, it will try to connect again 5 times.
    If it still fails, it will exit the program.
    """
    # Try and connect to the database 5 times.
    for _ in range(5):
        try:
            database = mysql.connector.connect(user=SQL_VARS.USER,
                                               password=SQL_VARS.PASSWORD,
                                               host=SQL_VARS.HOST,
                                               database=SQL_VARS.DATABASE)
            return database

        # If it fails, print an error message.
        except mysql.connector.Error:
            print("Failed to connect to the database. Retrying...")
        sleep(2)
    sys.exit()


if __name__ == "__main__":
    # Try and connect to the database.
    conn = connection()
    # Create a cursor.
    cursor = conn.cursor()
    # If it succeeds, create a new instance of the Casino class.
    casino = Casino()
    casino.login_menu()
    # Close the connection.
    conn.close()
    # Exit the program.
    sys.exit()
