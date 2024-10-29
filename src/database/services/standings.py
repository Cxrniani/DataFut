from ..utils.db_connection import get_db_connection
from ..utils.data_verification import record_exists

def insert_standing(fixture_id, team_name, position):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if the record already exists
            if not record_exists("SELECT 1 FROM standings WHERE fixture_id = %s AND team_name = %s", (fixture_id, team_name)):
                # Insert the new record
                cursor.execute(
                    "INSERT INTO standings (fixture_id, team_name, position) VALUES (%s, %s, %s)",
                    (fixture_id, team_name, position)
                )
                conn.commit()
                return True
            return False
    except Exception as e:
        print(f"Error inserting standing: {e}")
        return False

