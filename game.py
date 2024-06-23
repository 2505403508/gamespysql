#23552 Keith Guo
import sqlite3

database = "test.db"  # Name of the database file

def connect_to_database():  # Function to connect to the SQLite database
    try:
        return sqlite3.connect(database)  # Try to connect to the database
    except sqlite3.Error as e:  # If there is an error
        print(f"Database error: {e}")  # Print the error
        return None  # Return None if connection fails

def fetch_game_data(order_by):  # Function to fetch game data, ordered by a specified column
    db = connect_to_database()  # Connect to the database
    if db:
        cursor = db.cursor()  # Create a cursor object
        try:
            cursor.execute(f"""
                SELECT game.game_name, game.game_memory, kinds.kind_kind
                FROM game
                JOIN kinds ON game.game_kinds = kinds.kind_id
                ORDER BY {order_by};  # Order the results by the specified column
            """)
            return cursor.fetchall()  # Fetch all results from the query
        except sqlite3.Error as e:  # If there is an error in the query
            print(f"Error fetching data: {e}")  # Print the error
        finally:
            db.close()  # Close the database connection

def fetch_games_by_memory(user_memory):  # Function to fetch games by memory usage
    db = connect_to_database()  # Connect to the database
    if db:
        cursor = db.cursor()  # Create a cursor object
        try:
            cursor.execute("""
                SELECT game.game_name, game.game_memory, kinds.kind_kind
                FROM game
                JOIN kinds ON game.game_kinds = kinds.kind_id
                WHERE game.game_memory <= ?;  # Only fetch games with memory less than or equal to user_memory
            """, (user_memory,))
            return cursor.fetchall()  # Fetch all results from the query
        except sqlite3.Error as e:  # If there is an error in the query
            print(f"Error fetching data: {e}")  # Print the error
        finally:
            db.close()  # Close the database connection

def fetch_games_by_kind(kind_id):  # Function to fetch games by kind ID
    db = connect_to_database()  # Connect to the database
    if db:
        cursor = db.cursor()  # Create a cursor object
        try:
            cursor.execute("""
                SELECT game.game_name, game.game_memory, kinds.kind_kind
                FROM game
                JOIN kinds ON game.game_kinds = kinds.kind_id
                WHERE game.game_kinds = ?;  # Only fetch games with the specified kind_id
            """, (kind_id,))
            return cursor.fetchall()  # Fetch all results from the query
        except sqlite3.Error as e:  # If there is an error in the query
            print(f"Error fetching data: {e}")  # Print the error
        finally:
            db.close()  # Close the database connection

def print_games(data):  # Function to print game data
    if data:  # If there is data to print
        print(" ______________________________________________________________________")
        print("| Game Name                      | Game Memory (GB)  | Game Kind       |")
        for row in data:  # Loop through each row of data
            print(f"| {row[0]:<30} | {row[1]:<17} | {row[2]:<15} |")  # Print each column in the row
        print("|________________________________|___________________|_________________|")
    else:
        print("No data available.")  # If there is no data, print a message

while True:  # Infinite loop to keep the program running until the user decides to exit
    user_input = input("\nWhat would you like to do?\n1. Print all games ordered by name\n2. Print all games ordered by kind\n3. Print all games ordered by memory\n4. Recommend games based on available memory\n5. Recommend games based on preferred kind\n6. Exit\n")
    if user_input == '1':
        print_games(fetch_game_data('game_name'))  # Print all games ordered by name
    elif user_input == '2':
        print_games(fetch_game_data('kind_kind'))  # Print all games ordered by kind
    elif user_input == '3':
        print_games(fetch_game_data('game_memory'))  # Print all games ordered by memory
    elif user_input == '4':
        try:
            user_memory = float(input("Enter the available memory of your computer (in GB): "))  # Get available memory from user
            print_games(fetch_games_by_memory(user_memory))  # Recommend games based on available memory
        except ValueError:
            print("Invalid input. Please enter a numerical value for memory in GB.")  # Handle invalid input
    elif user_input == '5':
        print("1. Action\n2. Indie\n3. RPG\n4. Survival")  # Display kind options
        kind_choice = input("Enter the number corresponding to your preferred kind: ")
        if kind_choice in ['1', '2', '3', '4']:
            print_games(fetch_games_by_kind(kind_choice))  # Recommend games based on preferred kind
        else:
            print("Invalid input. Please enter a number between 1 and 4.")  # Handle invalid input
    elif user_input == '6':
        break  # Exit the program
    else:
        print('That was not an option.\n')  # Handle invalid menu option