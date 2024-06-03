import sqlite3
database = "test.db"
def connect_to_database():
    try:
        return sqlite3.connect(database)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


def fetch_game_data(order_by):
    db = connect_to_database()
    if db:
        cursor = db.cursor()
        try:
            cursor.execute(f"""
                SELECT game.game_name, game.game_memory, kinds.kind_kind
                FROM game
                JOIN kinds ON game.game_kinds = kinds.kind_id
                ORDER BY {order_by};
            """)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            db.close()

def print_games(data):
    if data:
        print(" ______________________________________________________________")
        print("| Game Name                      | Game Memory | Game Kind       |")
        for row in data:
            print(f"| {row[0]:<30} | {row[1]:<11} | {row[2]:<15} |")
        print("|________________________________|_____________|_________________|")
    else:
        print("No data available.")


while True:
    user_input = input("\nWhat would you like to do?\n1. Print all games ordered by name\n2. Print all games ordered by kind\n3. Print all games ordered by memory\n4. Exit\n")
    if user_input == '1':
        print_games(fetch_game_data('game_name'))
    elif user_input == '2':
        print_games(fetch_game_data('kind_kind'))
    elif user_input == '3':
        print_games(fetch_game_data('game_memory'))
    elif user_input == '4':
        break
    else:
        print('That was not an option.\n')

