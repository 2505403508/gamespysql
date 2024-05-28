import sqlite3

def print_games():
    db = sqlite3.connect('test.db')
    cursor = db.cursor()
    cursor.execute("select game.game_name,kinds.kind_kind FROM game JOIN kinds ON game.game_kinds = kinds.kind_id")