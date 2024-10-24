import sqlite3

def get_db_connection():
    conn = sqlite3.connect('path/to/your/database.db')  # Especifique o caminho para o seu banco de dados
    return conn