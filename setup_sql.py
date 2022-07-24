import os
import random


if os.path.exists('./SQL_VARS.py'):
    os.remove('SQL_VARS.py')

if os.path.exists('./Crypto_key.py'):
    os.remove('Crypto_key.py')

user = input("Enter username: ")
password = input("Enter password: ")
host = input("Enter host: ")
database_name = input("Enter database name: ")

if len(user) < 1 or len(password) < 1 or len(database_name) < 1:
    print("Invalid input")
    exit()

print("\nCreating SQL_VARS.py...")
with open('SQL_VARS.py', 'w') as f:
    f.write(f"USER = '{user}'\n")
    f.write(f"PASSWORD = '{password}'\n")
    f.write(f"HOST = '{host}'\n")
    f.write(f"DATABASE = '{database_name}'\n")
print("SQL_VARS.py created...")

try:
    length = int(input("Enter length of key: "))
    if length < 1:
        print("Invalid input")
        exit()
except ValueError:
    print("Invalid input")
    exit()

print("Generating Crypto_key.py...")
CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
key = ''.join(random.choice(CHARACTERS) for _ in range(int(length)))
with open('Crypto_key.py', 'w') as f:
    f.write(f"KEY = '{key}'\n")
print("Crypto_key.py created...")
