from ..utils.db_connection import get_db_connection
from ..utils.data_verification import record_exists
from ..utils.db_connection import get_db_connection

def get_injuries(fixture_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT player_name, team_name, injury_reason, injury_type FROM injuries WHERE fixture_id = ?", (fixture_id,))
        injuries = cursor.fetchall()
        return [{'player_name': row[0], 'team_name': row[1], 'injury_reason': row[2], 'injury_type': row[3]} for row in injuries]
    except Exception as e:
        print(f"Erro ao buscar injuries: {e}")
        return []
    finally:
        if conn:
            conn.close()

def insert_injury(fixture_id, player_name, team_name, injury_reason, injury_type):
    if not record_exists("SELECT 1 FROM injuries WHERE fixture_id = ? AND player_name = ?", (fixture_id, player_name)):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO injuries (fixture_id, player_name, team_name, injury_reason, injury_type) 
            VALUES (?, ?, ?, ?, ?)''', 
            (fixture_id, player_name, team_name, injury_reason, injury_type))
        conn.commit()
        conn.close()