from ..utils.data_verification import record_exists
from ..utils.db_connection import get_db_connection

def get_standings(fixture_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Use a coluna 'position' em vez de 'rank'
        cursor.execute("SELECT team_name, position FROM standings WHERE fixture_id = ?", (fixture_id,))
        standings = cursor.fetchall()
        return [{'team_name': row[0], 'position': row[1]} for row in standings]
    except Exception as e:
        print(f"Erro ao buscar standings: {e}")
        return []
    finally:
        if conn:
            conn.close()


def insert_standing(fixture_id, team_name, position):
    if not record_exists("SELECT 1 FROM standings WHERE fixture_id = ? AND team_name = ?", (fixture_id, team_name)):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO standings (fixture_id, team_name, position) 
            VALUES (?, ?, ?)''', 
            (fixture_id, team_name, position))
        conn.commit()
        conn.close()