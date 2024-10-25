from DataFut.src.database.utils.db_connection import get_db_connection
from DataFut.src.database.utils.data_verification import record_exists

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