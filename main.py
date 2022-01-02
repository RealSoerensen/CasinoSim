from random import randint
import mysql.connector
import SQL_VARS
import cryptocode
from Crypto_key import KEY
import inspect
from time import sleep

class Casino:
    """
    Casino class
    """

    def login_menu(self):
        """
        Login menu.
        """
        menu = """
                Welcome to the casino!
                Do you want to login or register?
                1: Login.
                2: Register.
                3: Exit.
                """
        while True:
            print(inspect.cleandoc(menu))
            
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
        Register.
        """
        # Register a new user.
        print("Please register")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Check if username is already taken.
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user is not None:
            print("Username already taken!")
            return
            
        # Encrypt the password.
        try:
            password = cryptocode.encrypt(password, KEY)
        except:
            print("Error encrypting password!")
            return

        # Get user_id by len of user_id length.
        cursor.execute("SELECT * FROM users")
        user_id = len(cursor.fetchall())

        # Insert new user into database.
        query = "INSERT INTO users (username, password, balance, user_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, password, 1000, user_id))
        db.commit()
        print("User registered!")
        print("\n"*5)

    def login(self):
        """
        Login.
        """
        print("Please login")
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            
            # Find username in database.
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            # If username is not found.
            if user is None:
                print("User or/and password is incorrect!")
                continue
            # Decrypt password.
            try:
                pw = cryptocode.decrypt(user[1], KEY)
            except:
                print("User or/and password is incorrect!")
                continue
            # If password is incorrect.
            if password != pw:
                print("User or/and password is incorrect!")
                continue
            # If username and password is correct.
            else:
                self.username = username
                self.balance = user[2]
                self.user_id = user[3]
                break

        Casino.main_menu(self)

    def main_menu(self):
        """
        Main menu.
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
            print("\n"*10)
            self.balance = Casino.read_balance(self)
            print(f"Hello {self.username}! Your balance is ${self.balance}")
            print(inspect.cleandoc(game_menu))
            choice = input("Enter your choice: ")

            if choice == "1":
                print("\n"*5)
                Casino.scratch_card(self)
            elif choice == "2":
                print("\n"*5)
                Casino.roulette(self)
            elif choice == "3":
                print("\n"*5)
                Casino.blackjack(self)
            elif choice == "4":
                print("\n"*5)
                Casino.dices(self)
            elif choice == "5":
                print("\n"*5)
                Casino.settings(self)
            elif choice == "6":
                break
        
    def scratch_card(self):
        """
        Scratch card.
        """
        while True:
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

                # If XXXX.
                if symbol1 == symbol2 and symbol2 == symbol3 and symbol3 == symbol4:
                    Casino.bet_won(self, bet, 50)
                    continue

                # If XXYY.
                elif symbol1 == symbol2 and symbol3 == symbol4:
                    Casino.bet_won(self, bet, 15)
                    continue

                # If XXXY.
                elif symbol1 == symbol2 and symbol2 == symbol3:
                    Casino.bet_won(self, bet, 10)
                    continue
                
                # If XXYZ
                elif symbol1 == symbol2:
                    Casino.bet_won(self, bet, 1)
                    continue

                # If none of the above    
                Casino.bet_lost(bet)
                
            elif choice == "2":
                print("""Rules for scratch cards:
                Place a bet and you will receive a scratchcard.
                The scratchcard will have 4 symbols.
                If you have the same symbols, you will win 50 times your bet.
                If you have 3 of the same symbols, you will win 25 times your bet.
                If you have 2 of the same symbols, you will win 0.5 times your bet.""")
            
            elif choice == "3":
                break
    
    
    def roulette(self):
        """
        Play roulette.
        """
        while True:
            print("1: Place bet.\n2: Rules.\n3: Exit.")
            choice = input("Enter your choice: ")

            if choice == "1":
                # Place bet.
                bet = Casino.bet_func(self)
                # Get int as input from user
                guess = input("Enter a number between 0 and 36: ")
                # Check if number is valid.
                if not guess.isdigit() or int(guess) < 0 or int(function) > 36:
                    print("Invalid number!")
                    continue
                # Get random number.
                number = randint(0, 36)
                print(f"The number is: {number}! You guessed {guess}!")
                # If the guess is correct.
                if number == guess:
                    Casino.bet_won(self, bet, 36)
                    return
                # If the guess is incorrect.
                return Casino.bet_lost(bet)

            elif choice == "2":
                print("""Rules for roulette:
                Place a bet and you will receive a roulette.
                The roulette will have 36 numbers.
                If you guess the number, you will win 35 times your bet.""")

            elif choice == "3":
                break

    def blackjack(self):
        """
        Play blackjack.
        """

    def dices(self):
        """
        Roll dices.
        """
        while True:
            print("1: Place bet.\n2: Rules.\n3: Exit.")
            choice = input("Enter your choice: ")
            if choice == "1":
                # Place bet.
                bet = Casino.bet_func(self)            
                d1 = randint(1, 6)
                d2 = randint(1, 6)
                print(f"Dice 1: {d1}")
                print(f"Dice 2: {d2}")
                # If d1 and d2 are equal.
                if d1 == d2:
                    Casino.bet_won(self, bet, 6)
                    return
                # If d1 and d2 are not equal.
                return Casino.bet_lost(bet)

            elif choice == "2":
                print("""Rules for dices:
                Place a bet and roll the dice!
                If you roll the same number, you will win 6 times your bet.\n""")

            elif choice == "3":
                break
    
    def settings(self):
        """
        Settings.
        """
        while True:
            print("1: Change username.\n2: Change password.\n3: Reset Balance.\n4: Exit.")
            choice = input("Enter your choice: ")
            if choice == "1":
                # Change username.
                new_username = input("Enter your new username: ")
                if new_username != self.username:
                    # Check if username is already taken.
                    query = "SELECT * FROM users WHERE username = %s"
                    cursor.execute(query, (new_username,))
                    if cursor.fetchone() is not None:
                        print("Username already taken!")
                        continue
                    # Change the username.
                    query = "UPDATE users SET username = %s WHERE username = %s"
                    cursor.execute(query, (new_username, self.user_id))
                    db.commit()
                    self.username = new_username
                    print("Your username has been changed!")
                    continue

            elif choice == "2":
                # Change password.
                new_password = input("Enter your new password: ")
                query = "UPDATE users SET password = %s WHERE user_id = %s"
                cursor.execute(query, (cryptocode.encrypt(new_password), self.user_id))
                db.commit()
                print("Your password has been changed!")

            elif choice == "3":
                # Change balance.
                new_balance = 1000
                query = "UPDATE users SET balance = %s WHERE user_id = %s"
                cursor.execute(query, (new_balance, self.user_id))
                db.commit()
                print("Your balance has been reset!")
                    
            elif choice == "4":
                break

    def bet_func(self):
        """
        Bet
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
            # Check if the bet isnt bigger than the balance.
            if bet > self.balance:
                print("You don't have enough money!")
                return
            # Check if the bet isnt 0.
            if bet == 0:
                print("You can't bet 0!")
                continue
            # Check if the bet isnt negative.
            if bet < 0:
                print("You can't bet a negative number!")
                continue

            # Update the balance.
            new_balance = self.balance - bet
            query = "UPDATE users SET balance = %s WHERE user_id = %s"
            cursor.execute(query, (new_balance, self.user_id))
            db.commit()
            return bet

    def bet_won(self, bet, multiplier):
        """
        Bet won
        """
        # Read the balance.
        self.balance = Casino.read_balance(self)
        print(f"You won ${bet * multiplier}!")
        # Update the balance.
        # Multiply the bet by the multiplier and add to balance.
        new_balance = self.balance + (bet * multiplier)
        query = "UPDATE users SET balance = %s WHERE user_id = %s"
        cursor.execute(query, (new_balance, self.user_id))
        db.commit()
        sleep(2)

    def bet_lost(bet):
        """
        Bet lost
        """
        print(f"You lost ${bet}!")
        sleep(2)

    def read_balance(self):
        """
        Read balance.
        """
        # Read the balance from SQL and return it.
        query = "SELECT balance FROM users WHERE user_id = %s"
        cursor.execute(query, (self.user_id,))
        return cursor.fetchone()[0]


def connection():
    """
    Connect to the database.
    """
    # Try and connect to the database.
    try:
        db = mysql.connector.connect(user=SQL_VARS.USER,
            password=SQL_VARS.PASSWORD,
            host=SQL_VARS.HOST,
            database=SQL_VARS.DATABASE)
    # If it fails, print an error message.
    except mysql.connector.Error as err:
        if err.errno == mysql.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        exit(1)
    return db

if __name__ == "__main__":
    # Try and connect to the database.
    db = connection()
    # Create a cursor.
    cursor = db.cursor()
    # If it succeeds, create a new instance of the Casino class.
    casino = Casino()
    casino.login_menu()
    # Close the connection.
    db.close()