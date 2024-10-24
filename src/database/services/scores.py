from DataFut.src.database.utils.db_connection import get_db_connection

def insert_score(fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO scores (fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (fixture_id, halftime_home, halftime_away, fulltime_home, fulltime_away, extratime_home, extratime_away, penalty_home, penalty_away))
    
    conn.commit()
    conn.close()