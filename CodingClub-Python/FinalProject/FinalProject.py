import sqlite3
from sqlite3 import Error
import getpass
import stdiomask
import time


def create_connection(db_file):
    connect = None
    try:
        connect = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e,"Error")
    return connect

def createTable(connect):
    sql_create_table = """CREATE TABLE IF NOT EXISTS Account (
    USERNAME CHAR(20) PRIMARY KEY,
    PASSWORD CHAR(20) NOT NULL,
    WORDSCORRECT INT NOT NULL,
    TOTALWORDS INT NOT NULL);"""

    cur = connect.cursor()
    cur.execute(sql_create_table)

def playHangman(connect, username, correctWords, totalWords):
    print("Hello, ", username, " time to play Hangman!")
    hangWord = stdiomask.getpass("Enter a word that you would like the other player to guess: ")
    time.sleep(1)
    print("Start guessing.")
    guesses = ' '
    
    turns = 15


    while turns > 0:
        failed = 0

        for char in hangWord:
            if char in guesses:

                print(char)
            else:
                print("_")

                failed += 1
        if failed == 0:
            print("You won!")
            correctWords += 1
            totalWords += 1
            break
        
        guess = input("Guess a character: ")
        guesses += guess
    
        if guess not in hangWord:
          turns -= 1
          print ("Wrong")
          
          print("You have", turns, "more guesses")


        if turns == 0:
            print("you lose!")
            totalWords += 1

    sql = '''SELECT * FROM ACCOUNT'''
    curr = connect.cursor()
    curr.execute(sql)

    results = curr.fetchall()
    ##If both user and password math go to next menu with account information.
    for row in results:
     username = row[0]
     password = row[1]
     correct = row[2]
     total = row[3]
     if user == username:
         correctWords = correct
         totalWords = total
         greetingsMenu(username, correct, total)
##works remember to commit the database once a change is made otherwise no changes will appear in the database
def CreateAccount(connect):
    user = input("Please enter your desired username: ")
    password = stdiomask.getpass("Enter the desired password: ")

    sql = '''INSERT INTO Account(USERNAME, PASSWORD, WORDSCORRECT, TOTALWORDS)
    VALUES(?, ?, ?,?)'''

    curr = connect.cursor()
    curr.execute(sql,[user, password, 0, 0])
    connect.commit()

def greetingsMenu(connect, username, correctWords, totalWords):
    print("Please choose one of the following.")
    print("1. Show the amount of words guessed correctly ")
    print("2. Show win percentage ")
    choice = input("3. Play Hangman!")

    if choice == '1':
        print("You have guessed: ", correctWords, " correctly.")
    elif choice == '2':
        print("you have a current win percentage of: ", correctWords/totalWords, "%")
    elif choice == '3': 
        playHangman(connect, username, correctWords, totalWords)
    else: 
        print("Pleae enter a valid choice.")

def mainMenu(connect):


        print("Please Login or Create an Account")
        print("1. Login")
        choice = input("2. Create Account")

        if choice == '1':
            login(connect)
        elif choice == '2':
            CreateAccount(connect)
        else: 
            print("Invalid Choice, Please Enter a valid choice: ")

def login(connect):

    ##variables to store information 
    ##stores wins
    correctWords = ' '
    ##Stores amount of games played.
    totalWords = ' '
    
    user = input("Enter Username: ")
    passwordEntered = stdiomask.getpass("Enter password: ")

    sql = '''SELECT * FROM ACCOUNT'''
    curr = connect.cursor()
    curr.execute(sql)

    results = curr.fetchall()
    ##If both user and password math go to next menu with account information.
    for row in results:
     username = row[0]
     password = row[1]
     correct = row[2]
     total = row[3]
     if user == username:
         if passwordEntered == password:
             correctWords = correct
             totalWords = total
             greetingsMenu(connect, username, correct, total)
    else:
        print("Invalid username and password.")






if __name__ == '__main__':
    connect = create_connection("mydatabase.db")
    createTable(connect)
    mainMenu(connect)




