"""
Casino program that I made for my own use.
It was created to try and learn how to use the MySQL database.
"""

from random import randint
from inspect import cleandoc
from time import sleep
import sys
import mysql.connector
import cryptocode
import SQL_VARS
from Crypto_key import KEY

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
            print("\n"*5)
            print(cleandoc(menu))
            # Loop until user enters a valid choice.
            choice = input("Enter your choice: ")
            if choice == "1":
                Casino.login(self)

            elif choice == "2":
                Casino.register(self)

            elif choice == "3":
                break

    def register(self):
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

        # Check if username is already taken.
        if not Casino.check_username(self, username):
            sleep(2)
            return

        if not Casino.check_password(self, password):
            sleep(2)
            return

        # Get user_id by len of user_id length.
        cursor.execute("SELECT * FROM users")
        user_id = len(cursor.fetchall())

        # Insert new user into database.
        query = "INSERT INTO users (username, password, balance, user_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, cryptocode.encrypt(password, KEY), 1000, user_id))
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
            query = "SELECT * FROM users WHERE username = %s"
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
            choice = input("Enter your choice: ")
            if choice == "1":
                Casino.scratch_card(self)

            elif choice == "2":
                Casino.roulette(self)

            elif choice == "3":
                Casino.blackjack(self)

            elif choice == "4":
                Casino.dices(self)

            elif choice == "5":
                Casino.settings(self)

            elif choice == "6":
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
            choice = input("Enter your choice: ")
            if choice == "1":
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
                    Casino.bet_won(self, bet, 15)
                    continue

                # If XXXY.
                if symbol1 == symbol2 and symbol2 == symbol3:
                    Casino.bet_won(self, bet, 10)
                    continue

                # If XXYZ
                if symbol1 == symbol2:
                    Casino.bet_won(self, bet, 1)
                    continue

                # If none of the above.
                Casino.bet_lost(self, bet)

            elif choice == "2":
                rules = """Rules for scratch cards:
                Place a bet and you will receive a scratchcard.
                The scratchcard will have 4 symbols.
                If you have the same symbols, you will win 50 times your bet.
                If you have 3 of the same symbols, you will win 25 times your bet.
                If you have 2 of the same symbols, you will win 0.5 times your bet."""
                print(cleandoc(rules))

            elif choice == "3":
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
            choice = input("Enter your choice: ")
            if choice == "1":
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
                Casino.bet_lost(self, bet)

            elif choice == "2":
                rules = """Rules for roulette:
                Place a bet and you will receive a roulette.
                The roulette will have 36 numbers.
                If you guess the number, you will receive your bet multiplied by 36."""
                print(cleandoc(rules))

            elif choice == "3":
                break

            sleep(2)

    def blackjack(self):
        """
        Play blackjack.
        """
        print("Blackjack is not implemented yet!")

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
            choice = input("Enter your choice: ")
            if choice == "1":
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
                Casino.bet_lost(self,bet)

            elif choice == "2":
                rules = """Rules for dices:
                Place a bet and roll the dice!
                If you roll the same number, you will win 6 times your bet."""
                print(cleandoc(rules))

            elif choice == "3":
                break

        sleep(2)

    def coinflip(self):
        """
        Coinflip.
        """
        while True:
            print("\n"*5)
            print("1: Place bet.\n2: Rules.\n3: Exit.")
            choice = input("Enter your choice: ")
            if choice == "1":
                # Place bet.
                bet = Casino.bet_func(self)
                while True:
                    # Get number from user.
                    choice = input("Enter heads or tails: ")
                    # Check if guess is a number.
                    if choice.lower() == "heads" or choice.lower() == "tails":
                        break
                    print("Invalid input!\n The input has to be heads or tails.")

                if choice.lower() == "heads":
                    choice = 0
                else:
                    choice = 1

                # Get random number.
                number = randint(0, 1)
                # If number is 0.
                if number == choice:
                    Casino.bet_won(self, bet, 2)
                    continue

                # If number is 1.
                Casino.bet_lost(self, bet)

            elif choice == "2":
                rules = """Rules for coinflip:
                Place a bet and you will receive a coinflip.
                The coinflip will have 2 numbers.
                If you guess the number, you will win 2x of your bet."""
                print(cleandoc(rules))

            elif choice == "3":
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
            choice = input("Enter your choice: ")
            if choice == "1":
                new_username = input("Enter your new username: ")
                if Casino.change_username(self, new_username) is not None:
                    self.username = new_username
                    print("Your username has been changed!")

            elif choice == "2":
                # Change password.
                new_password = input("Enter your new password: ")
                if Casino.change_password(self, new_password) is not None:
                    print("Your password has been changed!")

            elif choice == "3":
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

            elif choice == "4":
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
                print("Invalid choice.")
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

    def bet_lost(self, bet):
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
            query = "SELECT balance FROM users WHERE user_id = %s"
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
        if not Casino.check_username(self, new_username):
            return None
        try:
            # Change the username.
            query = "UPDATE users SET username = %s WHERE user_id = %s"
            cursor.execute(query, (new_username, self.user_id))
            conn.commit()
        except mysql.connector.Error:
            print("Something went wrong!")
            return None
        return new_username

    def check_username(self, username):
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
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            if user is not None:
                print("Username is already taken!")
                return False
        except mysql.connector.Error:
            print("Something went wrong!")
            return False
        return True

    def change_password(self, new_password):
        """
        Function to change the password.
        First check the password in the check_password function.
        Then encrypt the password.
        Then send query to the SQL database with the new password.
        Return the new password.
        """
        # Check if the password is valid.
        if not Casino.check_password(self, new_password):
            return None
        # Encrypt the password.
        new_password = cryptocode.encrypt(new_password, KEY)
        try:
            # Change the password.
            query = "UPDATE users SET password = %s WHERE user_id = %s"
            cursor.execute(query, (new_password, self.user_id))
            conn.commit()
        except mysql.connector.Error:
            print("Something went wrong!")
            return None
        return new_password

    def check_password(self, password):
        """
        Function to check if the password is valid.
        """
        if len(password) < 8:
            print("Password must be at least 8 characters long!")
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
    # Try and connect to the database.
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
