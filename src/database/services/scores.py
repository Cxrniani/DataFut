from ..utils.db_connection import get_db_connection
from ..utils.data_verification import record_exists

def insert_score(fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, 
                 extratime_home, extratime_away, penalty_home, penalty_away):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if the record already exists
            if not record_exists("SELECT 1 FROM scores WHERE fixture_id = %s", (fixture_id,)):
                # Insert the new record
                cursor.execute('''
                    INSERT INTO scores (fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, 
                                        extratime_home, extratime_away, penalty_home, penalty_away)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, 
                      extratime_home, extratime_away, penalty_home, penalty_away))
                conn.commit()
                return True
            return False
    except Exception as e:
        print(f"Error inserting score: {e}")
        return False

def get_score(fixture_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away FROM scores WHERE fixture_id = %s", (fixture_id,))
            score = cursor.fetchone()
            if score:
                return {
                    'halftime_home': score[0],
                    'halftime_away': score[1],
                    'fulltime_home': score[2],
                    'fulltime_away': score[3],
                    'extratime_home': score[4],
                    'extratime_away': score[5],
                    'penalty_home': score[6],
                    'penalty_away': score[7]
                }
            return None
    except Exception as e:
        print(f"Error fetching score: {e}")
        return None