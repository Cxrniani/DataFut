from DataFut.src.database.utils.db_connection import get_db_connection
from DataFut.src.database.utils.data_verification import record_exists

def insert_score(fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away):
    if not record_exists("SELECT 1 FROM scores WHERE fixture_id = ?", (fixture_id,)):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scores (fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away))
        conn.commit()
        conn.close()