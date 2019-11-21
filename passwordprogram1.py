#!/usr/bin/env python3

import sqlite3
import sys

def welcome_message():
    """Displays welcome message."""
    print("+-----------------------------------------+")
    print("|      Welcome to the Password Manager    |")
    print("+-----------------------------------------+")

id = 0

def create_account(username, password):
    """Creates a user account."""
    conn = sqlite3.connect("passwordDB.sqlite3")  # connect to the database

    max_id_query = "SELECT max(userID) FROM loginCredentials"  # get the most recently created accounts id
    max_id_obj = conn.execute(max_id_query)
    max_id_tuple = max_id_obj.fetchall()
    try:
        max_id = int(max_id_tuple[0][0])  # store most recent id
    except:
        max_id = 0

    id = max_id + 1  # create newest id

    create_user_insert = "INSERT INTO loginCredentials(userID, username, password) VALUES({A}, \"{B}\", \"{C}\")".format(A = id, B = username, C = password)

    cur = conn.cursor()
    cur.execute(create_user_insert)  # execute the creation
    conn.commit()  # commit changes to the database
    conn.close()  # close database connection


def validate_user(username, password):
    """Validates the user identity using information from database."""
    conn = sqlite3.connect("passwordDB.sqlite3")  # connect to the database

    username_query = "SELECT username FROM loginCredentials WHERE username = \"{A}\"".format(A = username)
    username_query_obj = conn.execute(username_query)  # execute query that checks for valid username
    username_tuple = username_query_obj.fetchone()  # store results of query - in a tuple
    try:
        username_result = username_tuple[0]  # if query returns a result, store it as a string
    except:
        username_result = ""  # if query returns no results/an error, set value as empty string

    password_query = "SELECT password FROM loginCredentials WHERE username = \"{A}\"".format(A = username)
    password_query_obj = conn.execute(password_query)  # execute query that checks for valid password
    password_tuple = password_query_obj.fetchone()
    try:
        password_result = password_tuple[0] # if query returns a result, store it as a string
    except:
        password_result = ""  # if query returns no results/an error, set value as empty string

    if username == username_result and password == password_result:
        return True
    else:
        return False

    conn.close()  # close database connection

def insert_data(username):
    """Insert the user provided data."""
    conn = sqlite3.connect("passwordDB.sqlite3") # connect to the database

    userID_query = "SELECT userID FROM loginCredentials WHERE username = \"{A}\"".format(A = username)
    userID_query_obj = conn.execute(userID_query)  # execute query that checks for valid password
    userID_tuple = userID_query_obj.fetchone()
    try:
        userID_result = userID_tuple[0] # if query returns a result, store it as a string
    except:
        userID_result = ""  # if query returns no results/an error, set value as empty string

    print("RESULT:", userID_result)
    print("Please enter your chosen credentials:")
    newUsername = input("Enter username: ")
    password = input ("Enter password: ")
    insert_command = "INSERT INTO userData(userID, username, password) VALUES ({A}, \"{B}\", \"{C}\")".format(A = userID_result, B = newUsername, C = password)
    conn.execute(insert_command)
    conn.commit()
    conn.close()
    print()
    print("Inserting data...")
    print()
    # try:
    #
    # except:
    #     print("Incorrect format. Exiting this option...")
    #     print()


def display_data(username):
    """Gets table contents."""
    conn = sqlite3.connect("passwordDB.sqlite3") # connect to the database

    userID_query = "SELECT userID FROM loginCredentials WHERE username = \"{A}\"".format(A = username)
    userID_query_obj = conn.execute(userID_query)  # execute query that checks for valid password
    userID_tuple = userID_query_obj.fetchone()
    try:
        userID_result = userID_tuple[0] # if query returns a result, store it as a string
    except:
        userID_result = ""  # if query returns no results/an error, set value as empty string

    get_data_command = "SELECT * FROM userData WHERE userID = \"{A}\"".format(A = userID_result) # query that gets the results from the given table

    result = conn.execute(get_data_command) # executes the querys
    data = result.fetchall()

    for i in data:
        print(i) # prints query results

    conn.close() # close DB connection

def main():
    decision = int(input("\nType 1 to login. Type 2 to create an account: "))
    if decision == 1:
        print("Enter your account credentials:")
        username = input("Enter username: ")
        password = input ("Enter password: ")
        result = validate_user(username, password)
        if result == True:
            print("\nSuccessful Login!\n")
            loginDecision = int(input("\nType 1 to display passwords. Type 2 to add a password: "))
            if loginDecision == 1:
                display_data(username)
            elif loginDecision == 2:
                insert_data(username)
        else:
            main()
    elif decision == 2:
        print("Please create an account:")
        username = input("Enter username: ")
        password = input ("Enter password: ")
        create_account(username, password)
        main()
    else:
        sys.exit()
welcome_message()
main()
