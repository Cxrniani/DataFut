from DataFut.src.database.utils.db_connection import get_db_connection
from DataFut.src.database.utils.data_verification import record_exists

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