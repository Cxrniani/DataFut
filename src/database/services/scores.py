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