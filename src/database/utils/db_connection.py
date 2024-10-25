import sqlite3

def get_db_connection():
    conn = sqlite3.connect('DataFut\src\database\datafut.db')
    return conn