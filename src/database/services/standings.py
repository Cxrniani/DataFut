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
    
def get_standings(fixture_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT team_name, position FROM standings WHERE fixture_id = ?", (fixture_id,))
        standings = cursor.fetchall()
        return [{'team_name': row[0], 'position': row[1]} for row in standings]
    except Exception as e:
        print(f"Erro ao buscar standings: {e}")
        return []
    finally:
        if conn:
            conn.close()

