from ..utils.db_connection import get_db_connection
from ..utils.data_verification import record_exists
from ..utils.db_connection import get_db_connection

def get_score(fixture_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away FROM scores WHERE fixture_id = ?", (fixture_id,))
        score = cursor.fetchone()
        if score:
            return {
                'halftime_home': score[0], 'halftime_away': score[1],
                'fulltime_home': score[2], 'fulltime_away': score[3],
                'extratime_home': score[4], 'extratime_away': score[5],
                'penalty_home': score[6], 'penalty_away': score[7]
            }
        return None
    except Exception as e:
        print(f"Erro ao buscar score: {e}")
        return None
    finally:
        if conn:
            conn.close()

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