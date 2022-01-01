from random import randint
import os
import sqlite3

def scratch_card():
    """
    Scratch card.
    """
    while True:
        print("1: Place bet.\n2: Rules.\n3: Exit.")
        while True:
            try:
                choice = int(input("Enter your choice: "))
                break
            except ValueError:
                print("Invalid choice.")

        if choice == "1":
            bet = bet_func()
            symbols = ["♠", "♥", "♦", "♣"]
            symbol_1, symbol_2, symbol_3, symbol_4 = symbols[randint(0,3)], symbols[randint(0,3)], symbols[randint(0,3)], symbols[randint(0,3)]

            print(f"Your card is: {symbol_1}{symbol_2}{symbol_3}{symbol_4}")

            if symbol_1 == symbol_2 and symbol_2 == symbol_3 and symbol_3 == symbol_4:
                bet_won(bet, 50)
                return

            elif symbol_1 == symbol_2 and symbol_2 == symbol_3:
                bet_won(bet, 15)
                return
            
            elif symbol_1 == symbol_2:
                bet_won(bet, 0.5)
                return
            return bet_lost(bet)
            
        elif choice == "2":
            print("\n")*5
            print("""Rules for scratch cards:\n
            Place a bet and you will receive a scratchcard.\n
            The scratchcard will have 4 symbols.\n
            If you have the same symbols, you will win 50 times your bet.\n
            If you have 3 of the same symbols, you will win 25 times your bet.\n
            If you have 2 of the same symbols, you will win 0.5 times your bet.\n""")
        
        elif choice == "3":
            break
    
    
def roulette():
    """
    Play roulette.
    """
    while True:
        print("1: Place bet.\n2: Rules.\n3: Exit.")
        while True:
            try:
                choice = int(input("Enter your choice: "))
                break
            except ValueError:
                print("Invalid choice.")

        if choice == 1:
            bet = bet_func()
            while True:
                try:
                    guess = int(input("Guess the number: "))
                    break
                except ValueError:
                    print("Invalid number!")
            
            number = randint(0, 36)
            print(f"The number is: {number}! You guessed {guess}!")
            if number == int(guess):
                bet_won(bet, 36)
                return
            return bet_lost(bet)

        elif choice == 2:
            print("\n")*5
            print("""Rules for roulette:\n
            Place a bet and you will receive a roulette.\n
            The roulette will have 36 numbers.\n
            If you guess the number, you will win 35 times your bet.\n""")

        elif choice == 3:
            break

def blackjack():
    """
    Play blackjack.
    """

def dices():
    """
    Roll dices.
    """
    while True:
        print("1: Place bet.\n2: Rules.\n3: Exit.")
        while True:
            try:
                choice = int(input("Enter your choice: "))
                break
            except ValueError:
                print("Invalid choice.")

        if choice == 1:
            bet = bet_func()            
            d1 = randint(1, 6)
            d2 = randint(1, 6)
            print(f"Dice 1: {d1}")
            print(f"Dice 2: {d2}")
            if d1 == d2:
                bet_won(bet, 6)
                return
            return bet_lost(bet)

        elif choice == 2:
            print("\n")*5
            print("""Rules for dices:\n
            Place a bet and roll the dice!\n
            If you roll the same number, you will win 6 times your bet.\n""")

        elif choice == 3:
            break
    
def bet_func():
    """
    Bet
    """
    balance = read_balance()
    bet = int(input("Enter your bet: "))
    if bet > balance:
        print("You don't have enough money!")
        return
    with open("balance.txt", "w") as f:
        f.write(str(balance - bet))
    return bet

def bet_won(bet, multiplier):
    """
    Bet won
    """
    balance = read_balance()
    print(f"You won ${bet * multiplier}!")
    with open("balance.txt", "w") as f:
        f.write(str(balance + bet * multiplier))

def bet_lost(bet):
    """
    Bet lost
    """
    print(f"You lost ${bet}!")

def main():
    """
    Main function
    """
    while True:
        balance = read_balance()
        print(f"Your balance is ${balance}")
        print("""
        1. Scratch a card.
        2. Play roulette.
        3. Play blackjack.
        4. Roll dices.
        5. Exit.
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            scratch_card()
        elif choice == "2":
            roulette()
        elif choice == "3":
            blackjack()
        elif choice == "4":
            dices()
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

def read_balance():
    """
    Read balance.
    """
    if os.path.exists("balance.txt"):
        with open("balance.txt", "r") as f:
            balance = int(f.read())
    else:
        balance = 1000
    return balance

def login():
    with sqlite3.connect("casino.popsql.io") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        for user in users:
            print(user)

def register():
    print()

if __name__ == "__main__":
    print("""Welcome to the casino!\n
    Do you want to login or register?\n
    1: Login.\n
    2: Register.\n""")
    
    while True:
        try:
            choice = int(input("Enter your choice: "))
            break
        except ValueError:
            print("Invalid choice.")
        
    if choice == 1:
        login()
    elif choice == 2:
        register()

